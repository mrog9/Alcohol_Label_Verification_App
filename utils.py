import numpy as np
import cv2
import easyocr

def run_ocr(file_obj):
    
    file_bytes = np.frombuffer(file_obj.read(), np.uint8)

    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    reader = easyocr.Reader(['en'])

    results = reader.readtext(image)

    text_list = []

    for (bbox, text, confidence) in results:
        
        text_list.append(text)

    joined_chars = "".join(text_list).lower()

    return joined_chars, text_list

def validate_form(brand, prod, alc, net, file):

    fail_str = ""

    if not brand:

        fail_str = fail_str + " Brand Name cannot be empty."

    else:

        brand_nm_list = brand.split(" ")

    if not prod:

        fail_str = fail_str + " Product Type cannot be empty."

    if not file:

        fail_str = fail_str + " A picture in appropriate format must be uploaded."

    return fail_str, brand_nm_list


def validate_labels(brand, prod, alc, net, file):

    fail_str, brand_nm_list = validate_form(brand, prod, alc, net, file)
    text = ""
    ocr_list = []

    if not fail_str:

        try:

            text, ocr_list = run_ocr(file)

            flag = False

            for b_nm in brand_nm_list:

                if b_nm not in text:

                    flag = True

            if flag:

                fail_str = fail_str + " Brand name is not in image."

            if prod not in text:

                fail_str = fail_str + " Product type is not in image."

            if alc not in text:

                fail_str = fail_str + " Alcohol content is not in image."

            if net not in text:

                fail_str = fail_str + " Net contents is not in image."

    

            if not fail_str:

                fail_str = "success!"
        
        except:

            fail_str = fail_str + " File must be in appropriate format"

    return fail_str, ocr_list


