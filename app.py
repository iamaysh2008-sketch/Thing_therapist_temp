from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>🔮 Thing Therapist</h1><p>Because even things need therapy.</p>"

if __name__ == "__main__":
    app.run(debug=True)
