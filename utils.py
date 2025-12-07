from PIL import Image, ImageFilter, ImageEnhance
import io
import pytesseract

def run_ocr(file_obj, lang="eng"):
    # Load image from file object
    img = Image.open(io.BytesIO(file_obj.read())).convert("L")  # grayscale
    
    # Optional preprocessing
    img = img.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)

    # Run OCR
    text = pytesseract.image_to_string(img, lang=lang)

    # Normalize output
    cleaned_text = text.strip().lower()
    return cleaned_text

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


