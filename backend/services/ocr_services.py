import os
import base64
import json
from typing import List, Dict, Any, Optional
from fastapi import UploadFile
from dotenv import load_dotenv
import pandas as pd
import io
from .llm_service import get_llm_service
import re
from tempfile import NamedTemporaryFile
from pdf2image import convert_from_path
import asyncio


# Load environment variables
load_dotenv()

class OCRService:
    def __init__(self):
        self.llm_service = get_llm_service()
        
    async def encode_image(self, image_file):
        """Encode image to base64"""
        # If image_file is already bytes, just encode it
        if isinstance(image_file, bytes):
            return base64.b64encode(image_file).decode("utf-8")
        # If it's a file-like object, read it
        if hasattr(image_file, 'read'):
            contents = image_file.read()
            if asyncio.iscoroutine(contents):
                contents = await contents
            return base64.b64encode(contents).decode("utf-8")
        return None
    
    async def pdf_to_images(self, pdf_file: UploadFile) -> List[dict]:
        """
        Convert a PDF UploadFile to a list of dicts with the original PDF filename and the image file-like object.
        Each dict: { 'pdf_filename': ..., 'image': ... }
        """
        # Save the PDF to a temporary file
        temp_pdf = NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_pdf.write(await pdf_file.read())
        temp_pdf.close()

        # Convert PDF to images (one per page)
        images = convert_from_path(temp_pdf.name)
        image_files = []
        for i, image in enumerate(images):
            temp_img = NamedTemporaryFile(delete=False, suffix=".jpg")
            image.save(temp_img, format="JPEG")
            temp_img.close()
            f = open(temp_img.name, "rb")
            class SimpleFile:
                def __init__(self, file, name):
                    self.file = file
                    self.name = name
                def read(self):
                    return self.file.read()
                def close(self):
                    self.file.close()
            image_files.append({
                'pdf_filename': pdf_file.filename,
                'image': SimpleFile(f, temp_img.name)
            })
        return image_files
    
    async def parse_document(self, document_file: UploadFile) -> Dict[str, Any]:
        """Parse document (PDF only) into structured data"""
        try:
            print(f"Processing document: {document_file.filename}")
            content_type = document_file.content_type or ""
            file_extension = document_file.filename.split('.')[-1].lower() if document_file.filename else ''

            # Check if it's a PDF
            is_pdf = file_extension == 'pdf' or 'pdf' in content_type.lower()

            if is_pdf:
                print("Processing as PDF document - converting to images")
                document_file.file.seek(0)
                try:
                    images = await self.pdf_to_images(document_file)
                    print(f"Converted to {len(images)} images")
                    
                    if not images:
                        return {
                            "document_type": "PDF",
                            "markdown_content": "",
                            "items": [],
                            "error": "No images extracted from PDF"
                        }
                    
                    all_markdown = ""
                    for idx, image_file in enumerate(images):
                        try:
                            print(f"Processing image {idx + 1}/{len(images)}")
                            # Get the actual file object from our SimpleFile wrapper
                            image = image_file['image']
                            image_data = image.read()  # Read the bytes directly
                            
                            # Encode without awaiting
                            image_base64 = base64.b64encode(image_data).decode("utf-8")
                            
                            messages = [
                                {"role": "system", "content": """
                                You are an OCR assistant powered by a Vision-Language Model. Your job is to extract text and formatting information from any document, regardless of its format (images, PDFs, handwritten notes, etc.). You must output all extracted content in a well-organized Markdown document.
                                Key requirements:
                                Comprehensive Extraction: Capture every bit of text present in the document.
                                Structured Markdown Output: Organize the extracted text into a structured Markdown format.
                                Formatting Preservation:
                                Headers: Convert document headers into Markdown headers (using #, ##, etc.).
                                Footers: Identify and annotate footers appropriately.
                                Tables: Recognize tables and render them using Markdown table syntax.
                                Additional Features: Include lists, bold or italic text, page breaks, and any other formatting cues that can be represented in Markdown.
                                Detail-Oriented: Ensure that nothing is omitted—extract and present all available information from the document.
                                Your final output should be a single, structured Markdown document that faithfully represents both the content and the formatting of the original input.
                                """},
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": "Please extract all text and formatting from this image and present it as a well-structured Markdown document."},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                                    ]
                                }
                            ]
                            
                            response = await self.llm_service.generate_vision(messages)
                            print(f"Got response for image {idx + 1}, length: {len(response)}")
                            all_markdown += response + "\n"
                            
                        except Exception as e:
                            print(f"Error processing image {idx + 1}: {str(e)}")
                            continue
                    
                    return {
                        "document_type": "PDF",
                        "markdown_content": all_markdown,
                        "items": []
                    }
                    
                except Exception as e:
                    print(f"Error in PDF processing: {str(e)}")
                    return {
                        "document_type": "PDF",
                        "markdown_content": "",
                        "items": [],
                        "error": str(e)
                    }
            else:
                return {
                    "error": "Only PDF files are supported.",
                    "document_type": file_extension.upper() if file_extension else "Unknown",
                    "items": []
                }
            
        except Exception as e:
            print(f"Error in parse_document: {str(e)}")
            return {
                "error": str(e),
                "document_type": file_extension.upper() if file_extension else "Unknown",
                "items": []
            }
    
    async def analyze_cvs(
        self,
        cv_contents: List[dict],  # Each dict: { "filename": ..., "content": ... }
        criteria: List[dict],     # Each dict: { "name": ..., "description": ... }
        job_description: str
    ) -> List[dict]:
        """
        For each CV, get scores for each criterion and a summary of the CV.
        Returns a list of dicts: { "filename": ..., "scores": ..., "summary": ... }
        """
        results = []
        for cv in cv_contents:
            # Build criteria string for the prompt
            criteria_str = "\n".join(
                f"- {c['name']}: {c['description']}" for c in criteria
            )

            # System prompt
            system_prompt = f"""
You are an expert CV analyzer with a focus on objective, data-driven evaluation. Your task is to analyze a CV and score it against specific criteria, always considering the job description when relevant.

Job Description:
{job_description}

Criteria (with descriptions):
{criteria_str}

Evaluation Guidelines:
1. Scoring System:
   - Use a 0-10 scale with one decimal point precision
   - 0: Completely missing or irrelevant
   - 5: Meets basic requirements
   - 10: Exceeds expectations significantly
   - When assigning scores, consider the full range of decimal values (e.g., 7.2, 8.3, 6.7, etc.) to best reflect nuanced differences in candidate performance.

2. Objectivity Requirements:
   - Base scores on concrete evidence from the CV
   - Avoid subjective interpretations
   - Consider quantifiable metrics when available

3. Job Description Integration:
   - For job-relevant criteria, explicitly map CV content to job requirements
   - For non-job-specific criteria (e.g., grammar), maintain objective standards

4. Response Format:
   - Each criterion must have a score (0-10 with one decimal point) and reasoning
   - The detailed summary should highlight key qualifications
   - The detailed summary should be around 200-300 words and structured as 2 paragraphs.
   - Maintain the exact JSON structure provided in the user prompt
"""

            # User prompt
            user_prompt = f"""CV Content:
{cv['content']}

First, extract the candidate's full name from the CV. If the name is not specified, use 'N/A'. Then provide your analysis in the following format:
{{
    "candidate": "<full name from CV or N/A>",
    "scores": {{
        "criterion1": {{
            "score": <number with one decimal point>,
            "explanation": "<brief reasoning for the score>"
        }},
        "criterion2": {{
            "score": <number with one decimal point>,
            "explanation": "<brief reasoning for the score>"
        }}
    }},
    "summary": "<2 paragraph detailed summary of key qualifications>"
}}
"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = await self.llm_service.generate_response(messages)
            # Clean up and parse response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            try:
                result = json.loads(response)
            except Exception as e:
                result = {"error": f"Failed to parse LLM response: {str(e)}", "raw_response": response}
            results.append({
                "filename": cv["filename"],
                **result
            })
        return results
    
