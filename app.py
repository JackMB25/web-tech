from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", questions=questions)


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.post("/about")
def getForm():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)