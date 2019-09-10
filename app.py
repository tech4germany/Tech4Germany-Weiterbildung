# example showing how to use Flask

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Tech4Germany!"

if __name__ == "__main__":
    app.run()