from flask import Flask
from flask import request
from flask import redirect, url_for
from flaskext.mysql import MySQL
from config import MYSQL_DATABASE_USER
from config import MYSQL_DATABASE_PASSWORD
from config import MYSQL_DATABASE_DB
from config import MYSQL_DATABASE_HOST
import json
from flask_sqlalchemy import SQLAlchemy
'''
app = Flask(__name__)
app.config['SECRET_KEY'] ='root'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3306/appUserData'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(app)
'''

mysql = MySQL()

# MySQL configurations
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = MYSQL_DATABASE_DB
app.config['MYSQL_DATABASE_HOST'] = MYSQL_DATABASE_HOST
mysql.init_app(app)

db = mysql.connect()

@app.route('/')
def hello_world():
    return 'Hello World!'

'''
login
Input: username, passwd
Function: Add the user information into database
'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        username = j_data['username']
        passwd = j_data['passwd']

        # login mysql & build the new table
        cursor = db.cursor()
        sql = "INSERT INTO users \
                VALUES ('%s', '%s')" % \
              (username, passwd)

        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

        db.close()

    return redirect(url_for('home'))


@app.route('/home', methods=['POST', 'GET'])
def home():
    return 'Home Page'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)