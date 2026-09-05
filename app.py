from flask import Flask, render_template, request
from openai import OpenAI
import os
import base64

app = Flask(__name__)

# OpenAI client
# It automatically uses the OPENAI_API_KEY
# from your PowerShell environment variable.
client = OpenAI()

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# WELCOME PAGE
# -----------------------------

@app.route("/")
def welcome():
    return render_template("welcome.html")


# -----------------------------
# OBJECT ANALYSER PAGE
# -----------------------------

@app.route("/analyser", methods=["GET", "POST"])
def analyser():

    result = ""

    if request.method == "POST":

        # Check if an image was uploaded
        if "image" not in request.files:
            return render_template(
                "index.html",
                result="No image was uploaded 😭"
            )

        image = request.files["image"]

        # Check if the user selected a file
        if image.filename == "":
            return render_template(
                "index.html",
                result="Please choose an object first! 🧐"
            )

        # Read the image directly
        image_data = image.read()

        # Convert image to Base64
        encoded_image = base64.b64encode(
            image_data
        ).decode("utf-8")

        try:

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
You are the world's most unnecessary
therapist for everyday objects.

Look carefully at the image and identify
the main object.

Pretend the object has feelings and
personal problems.

Give it funny, ridiculous and completely
unnecessary life advice related to what
the object actually does.

Also give the object a funny emotional
status with a percentage.

Use EXACTLY this format:

EMOTIONAL STATUS:
87% Existential Crisis 😭

OBJECT:
Chair 🪑

ADVICE:
You have spent your entire life supporting
everyone else. Maybe it is finally time to
take a stand for yourself.

Keep the response short, funny and playful.
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


        # Show a friendly error instead of
        # crashing the entire website
        except Exception as error:

            result = (
                "🚨 The Object Oracle had a problem 😭\n\n"
                + str(error)
            )


    return render_template(
        "index.html",
        result=result
    )


# -----------------------------
# RUN THE APP
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)