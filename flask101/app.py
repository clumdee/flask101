from __init__ import __version__
import logging
from flask import Flask, redirect, url_for, render_template

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
    content = dict()
    return render_template("index.html", content=content)

# pass part of URL as an argument
@app.get("/<name>-<lastname>")
def user(name, lastname):
    # return f"Hello {name}!"
    content = {'name':name, 'lastname':lastname}
    return render_template("index.html", content=content)

# straight redirect / redirect with url_for
@app.get("/admin")
def admin():
    # return redirect("/not-you")
    return redirect(url_for("user", name="not admin"))


if __name__ == '__main__':
    logger.debug(f"Running version {__version__}")
    app.run(debug=True)