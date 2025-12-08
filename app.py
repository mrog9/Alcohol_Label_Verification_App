from flask import Flask, request, render_template
from utils import *
import os

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("form.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_file():

    text = ""
    comment = ""

    if request.method == "POST":

        brand = request.form['brand'].lower()
        prod = request.form['product'].lower()
        alc = request.form['content'].lower()
        net = request.form['net'].lower()
        file = request.files["file"]

        comment = validate_form_input(brand, prod, alc, net, file)

        if not comment:

            text, comment = get_text_from_image(file)

        if not text and not comment:

            comment += "Take clearer picture. No text could be recognized."

        if not comment:

            comment = validate_label(text, brand, prod, alc, net)
      
    return render_template("form.html", text = text, comment = comment)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)