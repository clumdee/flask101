from flask import Flask, redirect, url_for


app = Flask(__name__)


# simple endpoint
@app.route("/")
def home():
    return "This is a home page"

# pass part of URL as an argument
@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

# straight redirect / redirect with url_for
@app.route("/admin")
def admin():
    # return redirect("/not-you")
    return redirect(url_for("user", name="not admin"))


if __name__ == '__main__':
    app.run()