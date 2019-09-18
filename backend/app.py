# example showing how to use Flask

from flask import Flask, render_template
import os

app = Flask(__name__)

# index route handler
# @app.route("/")
# def hello():
#     return "Hello Tech4Germany"

# index route handler with template
@app.route("/")
def hello():
    return render_template('example.html')

# custom route handler
@app.route("/<text>")
def custom_hello(text):
    return render_template('example2.html', text=text)

if __name__ == "__main__":
    app.run(debug=True)

    