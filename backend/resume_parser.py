import fitz 
import docx

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF resume."""
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX resume."""
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

if __name__ == "__main__":
    
    pdf_text = extract_text_from_pdf("sample_resume.pdf")
    print("PDF Resume Extracted:\n", pdf_text[:500]) 

    docx_text = extract_text_from_docx("sample_resume.docx")
    print("DOCX Resume Extracted:\n", docx_text[:500])
