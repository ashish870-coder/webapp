
from flowlang import run_code
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        code = request.form["code"]
        output = run_code(code)
    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)