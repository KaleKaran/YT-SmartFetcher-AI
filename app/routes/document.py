from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.utils.document import extract_pdf_text, extract_ppt_text
from app.utils.summary import generate_summary
from app.config.config import PDF_PPT_PROMPT
import os

document_bp = Blueprint('document', __name__)

@document_bp.route('/process_document', methods=['POST'])
def process_document():
    """
    Process uploaded documents (PDF, PPT).
    """
    if 'document' not in request.files:
        return "No file uploaded"

    file = request.files['document']
    if file.filename == '':
        return "No file selected"

    try:
        # Get base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        uploads_dir = os.path.join(base_dir, 'uploads')
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(uploads_dir, filename)

        os.makedirs(uploads_dir, exist_ok=True)

        file.save(file_path)

        if filename.endswith('.pdf'):
            text = extract_pdf_text(file_path)
        elif filename.endswith(('.ppt', '.pptx')):
            text = extract_ppt_text(file_path)
        else:
            return "Unsupported file format"

        if not text.strip():
            return "No text could be extracted from the document"

        summary = generate_summary(text, PDF_PPT_PROMPT)

        os.remove(file_path)  # Clean up after processing

        return render_template('document_result.html',
                               summary=summary,
                               text=text)

    except Exception as e:
        print(f"Error processing document: {str(e)}")
        return f"Error processing document: {str(e)}" 