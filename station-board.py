# coding: utf-8
# https: // qiita.com/nagataaaas/items/5c7c9ec4813fea85c40c


import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_uri = "mysql://b43919ff44eea8:28ebc9f7@us-cdbr-iron-east-01.cleardb.net/heroku_8a07ab701ff07b4"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class Board(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64))
    content = db.Column(db.String(256))
    timestamp = db.Column(db.DATETIME)

    def __repr__(self):
        return "Content<{}, {}, {}, {}>".format(self.id, self.name, self.content, self.timestamp)


@app.route("/", methods=["GET", "POST"])
def main_page():
    cont = Board.query.all()
    if request.method == "GET":
        return render_template("index.html", cont=cont)
    elif request.method == "POST":
        if not request.form["content"]:
            return render_template("index.html", cont=cont)
        try:
            postname = "ななしさん" if not request.form["name"] else request.form["name"]
            newpost = Board(
                name=postname, content=request.form["content"], timestamp=datetime.datetime.now())
            db.session.add(newpost)
            db.session.commit()
            cont = Board.query.all()
        except:
            db.rollback()
            raise
        return render_template("index.html", cont=cont)
    else:
        return render_template("index.html", cont=cont)


if __name__ == "__main__":
    app.run()
