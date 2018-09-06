# https: // qiita.com/nagataaaas/items/5c7c9ec4813fea85c40c

import datetime

from flask import Flask, render_template, request

from sqlalchemy import create_engine, Column, String, Integer, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)
engine = create_engine('sqlite:///app.db')
Base = declarative_base()


class Content(Base):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    content = Column(String)
    timestamp = Column(DATETIME)

    def __repr__(self):
        return "Content<{}, {}, {}, {}>".format(self.id, self.name, self.content, self.timestamp)


Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)
session = scoped_session(SessionMaker)


@app.route("/", methods=["GET", "POST"])
def main_page():
    cont = session.query(Content).all()
    if request.method == "GET":
        return render_template("index.html", cont=cont)
    elif request.method == "POST":
        if not request.form["content"]:
            return render_template("index.html", cont=cont)
        postname = "ななしさん" if not request.form["name"] else request.form["name"]
        newpost = Content(
            name=postname, content=request.form["content"], timestamp=datetime.datetime.now())
        session.add(newpost)
        session.commit()
        cont = session.query(Content).all()
        return render_template("index.html", cont=cont)
    else:
        return render_template("index.html", cont=cont)


if __name__ == "__main__":
    app.run(threaded=True)
