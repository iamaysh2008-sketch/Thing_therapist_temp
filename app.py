from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the Gemini Client once at startup to avoid garbage collection errors
api_key = os.getenv("GEMINI_API_KEY", "").strip()
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None


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

        try:
            # Verify API Key is configured
            if not client:
                raise RuntimeError(
                    "GEMINI_API_KEY is not configured. Add it to your .env or environment variables."
                )

            # Ask the AI using the persistent global client
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=[
                    """
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
""",
                    genai.types.Part.from_bytes(
                        data=image_data,
                        mime_type=image.mimetype or "image/jpeg",
                    ),
                ],
            )

            result = response.text

        # Show a friendly error instead of crashing the entire website
        except Exception as error:
            if "api key" in str(error).lower() or "authentication" in str(error).lower():
                result = (
                    "🔑 The Object Oracle's Gemini API key is invalid or has been "
                    "revoked. Update GEMINI_API_KEY in Vercel, then redeploy."
                )
            elif isinstance(error, RuntimeError):
                result = f"⚙️ Configuration problem: {error}"
            else:
                result = (
                    "🚨 The Object Oracle had a problem 😭\n\n"
                    f"Please try again in a moment. Error: {error}"
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