from flask import Flask, request, render_template
from utils import *

app = Flask(__name__)


@app.route("/")
def index():

    return render_template("form.html")

@app.route("/upload", methods=["POST"])
def upload_file():

    brand = request.form['brand'].lower()
    prod = request.form['product'].lower()
    alc = request.form['content'].lower()
    net = request.form['net'].lower()
    file = request.files["file"]
    
    comment_str, text= validate_labels(brand, prod, alc, net, file)

    return render_template("form.html", submission=comment_str, text = text)


if __name__ == "__main__":
    app.run(debug=True)



