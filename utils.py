import pytesseract
import io
from PIL import Image

# this method is to make sure the form fields are not empty. It goes through 
# each field and adds to the comment string if it is empty and returns the string.

def validate_form_input(b, p, a, n, f):

    comment = ""

    if not b:

        comment += "Brand name was not given.\n"

    if not p:

        comment += "Product type was not given.\n"

    if not a:

        comment += "Alcohol percentage was not given.\n"

    if not n:

        comment += "Net contents were not given.\n"

    if not f:

        comment += "A file was not uploaded."

    return comment

# this method recieves the uploaded file, reads it and then sends to pillow object
# to process it. It is put in a "try" so that if it fails for it not being in the
# correct format then a comment will be added telling the user it has to be in a certain format.
# if its successful, then the image is converted to gray scale and is upscaled before 
# pytesseract extracts text from the image. The text and comment is then returned.

def get_text_from_image(file_obj):

    fail_flag = False
    comment = ""
    text = ""

    img_bytes = file_obj.read()

    try:

        img = Image.open(io.BytesIO(img_bytes))

    except Exception as e:

        comment = "Make sure image is in either jpg, png, gif, bmp, tiff, webp, ico format."
        fail_flag = True

    if not fail_flag:

        img = img.convert("L")  # grayscale
        img = img.resize((img.width * 2, img.height * 2))  # upscale

        # OCR with PyTesseract
        text = pytesseract.image_to_string(img)

    return text, comment

# this method is going through each part of the text and assigning it to an appropriate field.
# there were many assumptions being made about the image being uploaded. It has to follow a specific
# pattern for this method to work correctly. Brand name is in all caps. Product name is follows and
# is before any number. Alcohol percentage precedes % symbol. Net contents is after everything else 
# and precedes "word" with L or mL in it. 

def extract_objs_from_text(text):

    text = text.replace("\n", " ")
    print(text)

    word_list = text.split(" ")

    brand_words_on_label = []
    prod_words_on_label = []
    alc_percent = ""
    net_contents = ""

    j = 0
    

    for i in range(len(word_list)):

        if word_list[i].isupper():

            brand_words_on_label.append(word_list[i])

        else:

            j = i
            break

    brand_on_label = " ".join(brand_words_on_label).lower()

    for i in range(j, len(word_list)):

        if "%" not in word_list[i]:

            prod_words_on_label.append(word_list[i])

        else:

            j=i
            break

    prod_on_label = " ".join(prod_words_on_label).lower()

    for c in word_list[j]:

        if c.isnumeric():

            alc_percent += c

    for i in range(j+1, len(word_list)):

        if 'L' in word_list[i]:

            net_contents = word_list[i-1] + word_list[i]

    print(brand_on_label)
    print(prod_on_label)
    print(alc_percent)
    print(net_contents)

    return brand_on_label, prod_on_label, alc_percent, net_contents

# this method validates the label. It uses the fields for the label extracted by
# the method above and compares with the fields on the form. Any mismatches will 
# be added to the comment string. If it gets through without any mismatches then it
# will output SUCCESS!

def validate_label(text, b, p, a, n):

    bl, pl, al, nl = extract_objs_from_text(text)

    comment = ""

    if not b.lower() == bl:

        comment += "Brand on form does NOT match brand on label.\n"

    if not p.lower() == pl:

        comment += "Product on form does NOT match product on label.\n"

    if not al.strip() == al:

        comment += "Alcohol percentage on form does NOT match percentage on label.\n"

    if not nl.strip() == nl:

        comment += "Net contents on form does NOT match net contents on label.\n"

    if not comment:

        comment = "SUCCESS!" \
    

    return comment

