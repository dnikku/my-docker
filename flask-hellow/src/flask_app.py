import sys
import logging
import pprint
from datetime import datetime

logging.basicConfig(stream=sys.stdout)


from flask import Flask, request
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World (root)!"

@app.route("/hh/")
def hello2():
    out = pprint.pformat(request.__dict__)
    out = ("Date: %r\n\n" % datetime.utcnow()) + out
    out = out.replace("\n", "<br>\n")
    return "<h1>Hello World (/hh/)!</h1>" + out


logging.info("Flask hellow created")

if __name__ == "__main__":
    app.run(port=8001, host="0.0.0.0")
