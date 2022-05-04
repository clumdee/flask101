import logging
from flask import Flask, redirect, url_for, render_template
from more_itertools import last

# simple log
logger_name = "app"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
# location w.r.t. working directory that calls this Flask app
hdler = logging.FileHandler(f"{logger_name}.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
hdler.setFormatter(formatter)
logger.addHandler(hdler)

app = Flask(__name__)


# simple endpoint
@app.get("/")
def home():
    logger.debug("calling home")
    # return "This is a home page"
    return render_template("index.html")

# pass part of URL as an argument
@app.get("/<name>-<lastname>")
def user(name, lastname):
    # return f"Hello {name}!"
    return render_template("index.html", name=name, lastname=lastname)

# straight redirect / redirect with url_for
@app.get("/admin")
def admin():
    # return redirect("/not-you")
    return redirect(url_for("user", name="not admin"))


if __name__ == '__main__':
    app.run(debug=True)