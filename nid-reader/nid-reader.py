import easyocr
import cv2
import re
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# Use EasyOCR for extracting text (using both Bengali and English)
reader = easyocr.Reader(['bn', 'en'])

def read_text_tesseract(img_location):
    # Load the image in grayscale mode
    img = cv2.imread(img_location, cv2.IMREAD_GRAYSCALE)
    myconfig = r"--psm 6 --oem 3"  # Config for pytesseract
    text = pytesseract.image_to_string(img, config=myconfig)
    return text

def process_tesseract_text(text):
    # Match patterns for Name, DOB, ID, Father, and Mother
    name = re.findall(r"Name: (.*)", text) or re.findall(r"নাম: (.*)", text)
    dob = re.findall(r"Date of Birth: (.*)", text) or re.findall(r"Date of Birth: (.*)", text)
    id_no = re.findall(r"NID No\n(.*)", text) or (r"ID NO: (.*)", text) or re.findall(r"ID No: (.*)", text) or re.findall(r"IDNO: (.*)", text) or re.findall(r"1D  (.*)", text) or re.findall(r"ID NO (.*)", text)
    father = re.findall(r"Father: (.*)", text) or re.findall(r"পিতা: (.*)", text)
    mother = re.findall(r"Mother: (.*)", text) or re.findall(r"মাতা: (.*)", text)
    
    return name, dob, id_no, father, mother

def extract_name(name):
    try:
        return re.sub('[^a-zA-Z ]+', '', name[0])
    except:
        return "Name not found"

def extract_dob(dob):
    try:
        return dob[0][0:11]
    except:
        return "DOB not found"

def extract_id(id_no):
    try:
        return "".join(filter(str.isdigit, id_no[0]))
    except:
        return "ID not found"

def extract_father(father):
    try:
        return father[0]
    except:
        return "Father not found"

def extract_mother(mother):
    try:
        return mother[0]
    except:
        return "Mother not found"

def read_text_easyocr(image_path):
    # Load the image in grayscale mode for EasyOCR
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    result_easyocr = reader.readtext(img)
    extracted_data = {
        "NameBn": "",
        "NameEn": "",
        "FatherBn": "",
        "MotherBn": "",
        "DOB": "",
        "ID": ""
    }
    
    for detection in result_easyocr:
        text = detection[1]
        if "নাম" in text and not extracted_data["NameBn"]:  
            extracted_data["NameBn"] = text.replace("নাম:", "").strip()
        if "Name" in text and not extracted_data["NameEn"]:
            extracted_data["NameEn"] = text.replace("Name", "").strip()
        if "পিতা" in text:
            extracted_data["FatherBn"] = text.replace("পিতা:", "").strip()
        if "মাতা" in text:
            extracted_data["MotherBn"] = text.replace("মাতা", "").strip()
        dob_match = re.search(r'\d{1,2} [A-Za-z]{3} \d{4}', text)
        if dob_match:
            extracted_data["DOB"] = dob_match.group(0).strip()
        nid_match = re.search(r'\d{10,20}', text)
        if nid_match:
            extracted_data["ID"] = nid_match.group(0).strip()
    
    return extracted_data

# Process image with both OCR methods
image_path = '../images/nid/aa2.jpg'  # Update this with the path to your image file

# First, get the raw text from Tesseract
text_tesseract = read_text_tesseract(image_path)
name, dob, id_no, father, mother = process_tesseract_text(text_tesseract)
tesseract_data = {
    "NameEn": extract_name(name),
    "DOB": extract_dob(dob),
    "ID": extract_id(id_no),
    "Father": extract_father(father),
    "Mother": extract_mother(mother)
}

# Next, get the raw text from EasyOCR
easyocr_data = read_text_easyocr(image_path)

# Merge results (ensure not to overwrite existing values)
final_result = {**easyocr_data, **{k: v for k, v in tesseract_data.items() if v}}

# Save the extracted raw text to a text file as it appears in the image
def save_raw_text_to_file(image_path, easyocr_data, tesseract_data, final_result):
    # Read the raw text from both OCR methods
    raw_text_easyocr = "\n".join([detection[1] for detection in reader.readtext(image_path)])
    raw_text_tesseract = text_tesseract  # The raw text from Tesseract OCR
    
    with open('extracted_raw_text.txt', 'w', encoding='utf-8') as file:
        file.write("Raw Text from EasyOCR:\n")
        file.write(raw_text_easyocr + "\n\n")
        
        file.write("Raw Text from Tesseract:\n")
        file.write(raw_text_tesseract + "\n\n")
        
        file.write("Merged Final Result:\n")
        for key, value in final_result.items():
            file.write(f"{key}: {value}\n")

# Save the raw text to the file
save_raw_text_to_file(image_path, easyocr_data, tesseract_data, final_result)

print(final_result)
