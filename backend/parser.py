import fitz
import re

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file using PyMuPDF
    """
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_resume_data(text):
    """
    Extract structured data (like name, email, phone number) from the resume text
    """
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zACharacters0-9.-]+\.[a-zA-Z]{2,}"
    phone_pattern = r"\+?[\d\(\)\- ]{10,15}"

    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)

    data =  {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "text" : text
    }
    return data

def parse_resume(file_path):
    """
    Parse the PDF resume and extract structured information like name, email, and phone
    """
    extracted_text = extract_text_from_pdf(file_path)
    data = extract_resume_data(extracted_text)
    print(data)
    return data

if __name__ == '__main__':
    parse_resume("uploads\Dheeraj_Gupta1.1.pdf")