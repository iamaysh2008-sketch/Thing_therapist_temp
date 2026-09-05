from flask import Flask, render_template, request
from openai import OpenAI
import os
import base64

app = Flask(__name__)

client = OpenAI()

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# WELCOME PAGE
@app.route("/")
def welcome():
    return render_template("welcome.html")


# OBJECT ANALYSER PAGE
@app.route("/analyser", methods=["GET", "POST"])
def analyser():

    result = ""

    if request.method == "POST":

        image = request.files["image"]

        if image:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                image.filename
            )

            image.save(filepath)

            with open(filepath, "rb") as image_file:

                encoded_image = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            response = client.responses.create(

                model="gpt-5.6-luna",

                input=[
                    {
                        "role": "user",

                        "content": [

                            {
                                "type": "input_text",

                                "text": """
Look at this image and identify the main object.

Then give that object funny and completely unnecessary life advice.

Treat the object as if it has feelings.

Make the advice connected to what the object does.

Keep the answer short.

Use this format:

OBJECT:
ADVICE:
"""
                            },

                            {
                                "type": "input_image",

                                "image_url":
                                f"data:image/jpeg;base64,{encoded_image}"
                            }
                        ]
                    }
                ]
            )

            result = response.output_text

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)