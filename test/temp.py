from flask import Flask, render_template

app = Flask(__name__)


@app.route("/hello", methods=['GET', 'POST'])
def Hello():
    message = "hello"
    return render_template("temp.html", temp=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8987, debug=True)
