from fpdf import FPDF
import io

def export_to_pdf(text: str) -> bytes:
    """
    Converts text to PDF format and returns bytes.
    
    Args:
        text (str): The markdown or plain text to convert.
        
    Returns:
        bytes: PDF data in bytes.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    # Simple formatting: Replace some common markdown with plain text for basic PDF compatibility
    # FPDF2 handles basic unicode, but let's ensure it doesn't break
    text_encoded = text.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 10, text_encoded)
    
    # Get bytearray of the PDF
    return bytes(pdf.output())

def export_to_md(text: str) -> str:
    """
    Wraps the text in basic Markdown layout.
    """
    return f"# Video Summary\n\n{text}\n"
