#import os
#import tempfile
#from typing import List
#from pdf2image import convert_from_bytes
#from fastapi import UploadFile
#import base64
#from io import BytesIO

#class PDFService:
#    def __init__(self):
#        # Check if poppler is installed (required for pdf2image)
#        try:
#            from pdf2image.exceptions import PDFInfoNotInstalledError
#            # This will raise an exception if poppler is not installed
#            convert_from_bytes(b'')
#        except PDFInfoNotInstalledError:
#            raise RuntimeError("Poppler is not installed. Please install it using: brew install poppler (macOS) or apt-get install poppler-utils (Linux)")

#    async def convert_pdf_to_images(self, pdf_file: UploadFile, dpi: int = 200) -> List[dict]:
#        """
#        Convert a PDF file to a list of images.
#        Each image is returned as a base64-encoded string.
        
#        Args:
#            pdf_file: The PDF file to convert
#            dpi: The DPI (dots per inch) for the output images
            
#        Returns:
#            A list of dictionaries containing the page number and base64-encoded image
#        """
#        try:
#            # Read the PDF file
#            pdf_bytes = await pdf_file.read()
            
#            # Convert PDF to images
#            images = convert_from_bytes(pdf_bytes, dpi=dpi)
            
#            # Convert images to base64
#            result = []
#            for i, image in enumerate(images):
#                # Convert PIL image to bytes
#                img_byte_arr = BytesIO()
#                image.save(img_byte_arr, format='PNG')
#                img_byte_arr = img_byte_arr.getvalue()
                
#                # Convert to base64
#                img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
                
#                result.append({
#                    "page_number": i + 1,
#                    "image": img_base64,
#                    "format": "PNG"
#                })
            
#            return result
            
#        except Exception as e:
#            raise Exception(f"Error converting PDF to images: {str(e)}") 