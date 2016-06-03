import sys
import logging
logging.basicConfig(stream=sys.stdout)


from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World (root)!"

@app.route("/route2/")
def hello2():
    return "Hello World (/route2/)!"


logging.info("Flask hellow created")

if __name__ == "__main__":
    app.run(port=8001, host="0.0.0.0")
