from flask import Flask, render_template, request
from openai import OpenAI
import os
import base64

app = Flask(__name__)


def get_openai_client():
    return OpenAI()


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

        image = request.files.get("image")

        if image and image.filename:

            # Convert image into a format
            # that the AI can understand
            encoded_image = base64.b64encode(
                image.read()
            ).decode("utf-8")


            # Ask the AI

            response = get_openai_client().responses.create(

                model="gpt-4o",

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
                                f"data:{image.mimetype or 'image/jpeg'};base64,{encoded_image}"
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