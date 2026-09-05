from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    advice = ""

    if request.method == "POST":

        object_name = request.form["object"].lower()

        if object_name == "chair":
            advice = "You've spent your whole life supporting everyone else. Maybe it's time to take a stand."

        elif object_name == "pillow":
            advice = "You carry everyone's dreams every night. Maybe you deserve some rest too."

        elif object_name == "shoe":
            advice = "Sometimes the best thing you can do is walk away."

        elif object_name == "bottle":
            advice = "Don't bottle up your emotions. Unless you're literally a bottle."

        else:
            advice = "I don't know what you are, but you deserve completely unnecessary advice."

    return render_template("index.html", advice=advice)


if __name__ == "__main__":
    app.run(debug=True)
