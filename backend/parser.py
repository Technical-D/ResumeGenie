import fitz
import re
import spacy
import json
from skill import skills_set

# Loading Countries and cities
with open('country_city_mapping.json', 'r', encoding="utf-8") as f:
    data = dict(json.load(f))

countries = list(data.keys())
indian_cities = list(data['India'])

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

def validate_name(name):    
    return len(name.split()) >= 2 and all(part.isalpha() for part in name.split())

def validate_city(city):
    if city.lower() in [c.lower() for c in indian_cities]:
        return True
    return False

def validate_country(country):
    if country.lower() in [c.lower() for c in countries]:
        return True
    return False

def extract_info_using_nlp(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    info = {"name": None, "city": None, "country": None}
    for ent in doc.ents:
        if ent.label_ == "PERSON" and validate_name(ent.text):
            info["name"] = ent.text
        
        if ent.label_ == "GPE":
            if validate_city(ent.text):
                info["city"] = ent.text

            if validate_country(ent.text):
                info["country"] = ent.text
        
    return info

def extract_skills(text):
    found_skills = [skill for skill in skills_set if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE)]
    return found_skills

def extract_resume_data(text):
    """
    Extract structured data from the resume text
    """
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zACharacters0-9.-]+\.[a-zA-Z]{2,}"
    phone_pattern = r"\+?[\d\(\)\- ]{10,15}"

    name, city, country= extract_info_using_nlp(text).values()
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    skills = extract_skills(text)
    data =  {
        "name" : name,
        "email": email.group(0).strip() if email else None,
        "phone": phone.group(0).strip() if phone else None,
        "skills": skills,
        "city" : city.strip(),
        "country": country.strip()
    }
    return data

def parse_resume(file_path):
    """
    Parse the PDF resume and extract structured information like name, email, and phone
    """
    extracted_text = extract_text_from_pdf(file_path)
    data = extract_resume_data(extracted_text)

    return data

if __name__ == '__main__':
    parse_resume("uploads\Dheeraj_Gupta1.1.pdf")