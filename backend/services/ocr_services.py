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


# Load environment variables
load_dotenv()

class OCRService:
    def __init__(self):
        self.llm_service = get_llm_service()
        
    async def encode_image(self, image_file):
        """Encode image to base64"""
        contents = await image_file.read()
        return base64.b64encode(contents).decode("utf-8")
    
    async def parse_document(self, document_file: UploadFile) -> Dict[str, Any]:
        """Parse document (CSV, Excel, PDF, etc.) into structured data"""
        contents = await document_file.read()
        content_type = document_file.content_type or ""
        file_extension = document_file.filename.split('.')[-1].lower() if document_file.filename else ''
        
        # Check if it's a PDF
        is_pdf = file_extension == 'pdf' or 'pdf' in content_type.lower()
        # Check if it's an image
        is_image = any(ext in file_extension for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']) or 'image' in content_type.lower()
        
        try:
            if file_extension == 'csv' or 'csv' in content_type.lower():
                print("Processing as CSV document")
                df = pd.read_csv(io.BytesIO(contents))
                return json.loads(df.to_json(orient="records"))
            
            elif file_extension in ['xls', 'xlsx'] or 'excel' in content_type.lower() or 'spreadsheet' in content_type.lower():
                print("Processing as Excel document")
                df = pd.read_excel(io.BytesIO(contents))
                return json.loads(df.to_json(orient="records"))
            
            elif is_pdf:
                # For PDFs, use the vision API directly instead of extracting text first
                print("Processing as PDF document - sending directly to vision API")
                
                # Convert PDF content to base64
                pdf_base64 = base64.b64encode(contents).decode("utf-8")
                
                # Use the vision model with the new prompt
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
                            {"type": "text", "text": "Please extract all text and formatting from this document and present it as a well-structured Markdown document."},
                            {"type": "image_url", "image_url": {"url": f"data:application/pdf;base64,{pdf_base64}"}}
                        ]
                    }
                ]
                
                response = await self.llm_service.generate_vision(messages)
                
                # Return the markdown response directly
                return {
                    "document_type": "PDF",
                    "markdown_content": response,
                    "items": []
                }
                    
            elif is_image:
                # Handle image-based documents (e.g., scanned documents)
                print("Processing as image document")
                
                # Convert image content to base64
                image_base64 = base64.b64encode(contents).decode("utf-8")
                
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
                
                # Return the markdown response directly
                return {
                    "document_type": "Image",
                    "markdown_content": response,
                    "items": []
                }
            
            else:
                return {
                    "error": f"Unsupported file type: {file_extension}",
                    "document_type": "Unknown",
                    "items": []
                }
                
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            return {
                "error": str(e),
                "document_type": file_extension.upper() if file_extension else "Unknown",
                "items": []
            }
    
    async def summarize_content(self, content: str, criteria: List[str]) -> Dict[str, Any]:
        """
        Summarize the content of a CV and score it against user criteria using LLM.
        Returns a structured response with scores for each criterion.
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert CV analyzer. Your task is to analyze a CV and score it against specific criteria.
                    For each criterion, provide a score from 0-10 and a brief explanation of why that score was given.
                    Return the response in a structured format with scores and explanations for each criterion."""
                },
                {
                    "role": "user",
                    "content": f"""Please analyze this CV content and score it against these criteria: {', '.join(criteria)}
                    
                    CV Content:
                    {content}
                    
                    Provide your analysis in the following format:
                    {{
                        "scores": {{
                            "criterion1": {{
                                "score": <number>,
                                "explanation": "<explanation>"
                            }},
                            "criterion2": {{
                                "score": <number>,
                                "explanation": "<explanation>"
                            }}
                        }}
                    }}"""
                }
            ]
            
            response = await self.llm_service.generate_response(messages)
            return response
            
        except Exception as e:
            print(f"Error summarizing content: {str(e)}")
            raise

    async def rank_cvs(self, cv_summaries: List[Dict[str, Any]], criteria: List[str]) -> List[Dict[str, Any]]:
        """
        Rank CVs based on their summaries and user criteria using LLM.
        Returns an ordered list of CVs with their rankings and scores.
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert CV ranking system. Your task is to compare multiple CVs and rank them based on how well they meet the specified criteria.
                    Consider the scores and explanations provided for each CV and provide a final ranking.
                    Return the response in a structured format with the ranked list of CVs."""
                },
                {
                    "role": "user",
                    "content": f"""Please rank these CVs based on these criteria: {', '.join(criteria)}
                    
                    CV Summaries:
                    {json.dumps(cv_summaries, indent=2)}
                    
                    Provide your ranking in the following format:
                    {{
                        "ranked_cvs": [
                            {{
                                "filename": "<filename>",
                                "overall_score": <number>,
                                "ranking": <number>,
                                "summary": "<brief explanation of why this CV was ranked at this position>"
                            }},
                            ...
                        ]
                    }}"""
                }
            ]
            
            response = await self.llm_service.generate_response(messages)
            
            
            # Clean up the response by removing markdown code block formatting
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]  # Remove ```json
            if response.startswith("```"):
                response = response[3:]  # Remove ```
            if response.endswith("```"):
                response = response[:-3]  # Remove ```
            response = response.strip()
            
            # Parse the JSON response
            result = json.loads(response)
            return result.get("ranked_cvs", [])            
        except Exception as e:
            print(f"Error ranking CVs: {str(e)}")
            raise
    
