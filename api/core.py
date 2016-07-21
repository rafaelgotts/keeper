from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route("/ping/hc")
def healt_check():
    return "{'status': 'OK'}"


if __name__ == "__main__":
    app.run()
