from flask import Flask, render_template

app = Flask(__name__)


def getContent():
    return [{'name': 'Tanaka', 'text': 'こんにちは'}, {'name': 'Kondo', 'text': 'Nice to meet you'}]


@app.route('/')
def index():
    return render_template('index.html', content=getContent())


if __name__ == '__main__':
    app.debug = True
    app.run()
