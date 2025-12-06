from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]  # get uploaded file
        if file:

            # url_api = "https://api.ocr.space/parse/image"
            # payload = {"apikey": "K81796487388957", "language": "eng"}
            # response = requests.post(url_api, data=payload, files={"file": file})
            # result = response.json()
            return str(file)
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)

