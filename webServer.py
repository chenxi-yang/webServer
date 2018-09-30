from flask import Flask
from flask import request
from flask import redirect, url_for
from flaskext.mysql import MySQL
from config import MYSQL_DATABASE_USER
from config import MYSQL_DATABASE_PASSWORD
from config import MYSQL_DATABASE_DB
from config import MYSQL_DATABASE_HOST
from markedWords import *
from helper import *
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
Input: username, password
Function: 
user login
if the user existed before, then check the password and log in the user;
else sign up the user.
'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        username = j_data['username']
        password = j_data['password']

        cursor = db.cursor()

        # check whether the user existed before
        check_operation = "SELECT 1 FROM users WHERE user_name = '%s'" % username
        result = get_one_row(cursor, check_operation)

        # sign up
        if result is None:
            get_last_insert_id_operation = "SELECT LAST_INSERT_ID();"
            result_last_insert_id = get_one_row(cursor, get_last_insert_id_operation)
            insert_operation = "INSERT INTO users \
                                            VALUES ('%s', '%s')" % \
                               (username, password)
            try:
                cursor.execute(insert_operation)
                db.commit()
            except:
                db.rollback()
            return redirect(url_for('home/\'%s\'')) % result_last_insert_id
        # log in
        else:
            # valid password
            if password == result["user_password"]:
                return redirect(url_for('home/\'%s\'')) % result["user_id"]
            # invalid password
            else:
                return WRONG_PASSWORD

        '''
        # user already existed
        if result.with_rows:
            result_set = cursor.fetchall()
            for row in result_set:
                # valid password
                if password == row["user_password"]:
                    return redirect(url_for('home/\'%s\'')) % row["user_id"]
                # invalid password
                else:
                    return WRONG_PASSWORD
        # new user
        else:
            get_last_insert_id_operation = "SELECT LAST_INSERT_ID();"

            insert_operation = "INSERT INTO users \
                                VALUES ('%s', '%s')" % \
                               (username, password)
            try:
                cursor.execute(insert_operation)
                db.commit()
            except:
                db.rollback()
        '''

    return redirect(url_for('error'))

@app.route('/wrong_password', methods=['POST', 'GET'])
def wrong_password():
    # TODO: wrong password handler
    return 0

@app.route('/home/<user_id>', methods=['POST', 'GET'])
def home_user_id():
    # TODO: return the records of the user with this user_id
    return 0

@app.route('/home/plan_setting/<user_id>', methods=['POST', 'GET'])
def home_plan_setting():
    # insert into user_plan
    cursor = db.cursor()
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        start_time = j_data['start_time']
        end_time = j_data['end_time']
        app_name = j_data['user_id']

        insert_plan_operation = "INSERT INTO user_plan \
                                    VALUES ('%s', '%s', '%s')" % \
                                    (start_time, end_time, app_name)
        try:
            cursor.execute(insert_plan_operation)
            db.commit()
        except:
            db.rollback()

    return 'Plan Set'

# TODO: get users' app usage history automatically

@app.route('/error')
def error():
    return 'Ooooooops, error happened.'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)