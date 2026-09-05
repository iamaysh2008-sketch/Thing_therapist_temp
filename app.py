from flask import Flask, render_template, request
from openai import OpenAI
import os
import base64

app = Flask(__name__)

client = OpenAI()

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------------
# WELCOME PAGE
# -------------------------------

@app.route("/")
def welcome():

    return render_template("welcome.html")


# -------------------------------
# OBJECT ANALYSER PAGE
# -------------------------------

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


            # Convert image into a format
            # that the AI can understand

            with open(filepath, "rb") as image_file:

                encoded_image = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")


            # Ask the AI

            response = client.responses.create(

                model="gpt-5.6-luna",

                input=[
                    {
                        "role": "user",

                        "content": [

                            {
                                "type": "input_text",

                                "text": """
Look carefully at this image and identify
the main object.

Pretend that this object is receiving
completely unnecessary therapy.

Give it funny and useless life advice.

Treat the object as if it has feelings,
emotions, and personal problems.

The advice should relate to what the
object actually does.

Also give the object a funny emotional
status with a random percentage.

Use EXACTLY this format:

EMOTIONAL STATUS:
(example: 87% Existential Crisis 😭)

OBJECT:
(example: Chair 🪑)

ADVICE:
(example: You have spent your entire life
supporting everyone else. Maybe it is time
to finally take a stand for yourself.)

Keep everything short, funny, and playful.
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


# -------------------------------
# RUN THE APP
# -------------------------------

if __name__ == "__main__":

    app.run(debug=True)