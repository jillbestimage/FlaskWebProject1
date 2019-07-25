"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
https: //kknews.cc/zh-tw/other/6one9nm.html
"""
# 
import sqlalchemy  
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flask import Flask,  Response, jsonify
app = Flask(__name__)

engine = sqlalchemy.create_engine("mysql+pymysql://root:eKsy1RJw!@127.0.0.1:3306/test", encoding="utf8", echo=True)
metadata = sqlalchemy.MetaData(bind = engine)
Base = declarative_base(metadata)

Session = sessionmaker(bind=engine)
session = Session()

class Worklist(Base):       
      __table__ = sqlalchemy.Table('worklist', metadata, autoload=True)

      def to_json(self):
          dict = self.__dict__
          if "_sa_instance_state" in dict:
              del dict["_sa_instance_state"]
              return dict

class Reportb(Base):
      __table__ = sqlalchemy.Table('reportb', metadata, autoload = True)

@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"

@app.route('/insertworklistone/<ACCNO>')
def insertworklistone(ACCNO):
    item = Worklist(ACCESSION_NUMBER = ACCNO, MODALITY = '')
    session.add(item)
    session.commit()
    return '建立單筆成功'

@app.route('/deleteworklistone/<ACCNO>')
def deleteworklistone(ACCNO):
    session.query(Worklist).filter(Worklist.ACCESSION_NUMBER==ACCNO).delete()
    session.commit()
    return 'DELETE成功'

@app.route('/queryworklistone/<ACCNO>')
def queryworklistone(ACCNO):
    userquery = session.query(Worklist).filter(Worklist.ACCESSION_NUMBER==ACCNO).all()
    result = []
    for comment in userquery:
        result.append(comment.to_json())
    return jsonify(result), 200

@app.route('/updateworklistone/<ACCNO>')
def updateworklistone(ACCNO):
    session.query(Worklist).filter(Worklist.ACCESSION_NUMBER==ACCNO).update({'PTN_ID':'001','MODALITY':'OT'})
    session.commit()
    return '修改成功'


if __name__ == '__main__':
#    import os
#    HOST = os.environ.get('SERVER_HOST', 'localhost')
#    try:
#        PORT = int(os.environ.get('SERVER_PORT', '5555'))
#    except ValueError:
#        PORT = 5555
#    app.run(HOST, PORT)
     app.run(host='0.0.0.0', port='5000')
