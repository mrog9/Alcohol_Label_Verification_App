import io
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from paddleocr import PaddleOCR

# Initialize PaddleOCR once (English only, CPU)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def run_ocr(file_obj):

    # Load image with Pillow
    img = Image.open(io.BytesIO(file_obj.read())).convert("RGB")

    # Optional preprocessing
    img = img.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)

    img_array = np.array(img)   # Pillow → NumPy

    # Run OCR
    results = ocr.ocr(img_array, cls=True)

    # Extract text
    text = " ".join([line[1][0] for line in results[0]])

    return text

def validate_form(brand, prod, alc, net, file):

    fail_str = ""
    brand_nm_list = []

    if not brand:

        fail_str = fail_str + " Brand Name cannot be empty."

    else:

        if len(brand.split(" ")) > 1:

            brand_nm_list = brand.split(" ")

        else:

            brand_nm_list.append(brand)

    if not prod:

        fail_str = fail_str + " Product Type cannot be empty."

    if not file:

        fail_str = fail_str + " A picture in appropriate format must be uploaded."

    return fail_str, brand_nm_list


def validate_labels(brand, prod, alc, net, file):

    fail_str, brand_nm_list = validate_form(brand, prod, alc, net, file)
    text = ""

    if not fail_str:

        try:

            text = run_ocr(file)

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
        
        except Exception as e:

            fail_str = fail_str + str(e)

    return fail_str, text


