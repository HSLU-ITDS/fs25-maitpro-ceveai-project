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
    
