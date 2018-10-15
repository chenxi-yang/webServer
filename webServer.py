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
from dbFieldIndex import *
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
        check_operation = "SELECT * FROM users WHERE user_username = '%s'" % username
        result = get_one_row(cursor, check_operation)
        user_id = -1

        # sign up
        if result is None:
            get_last_insert_id_operation = "SELECT MAX(user_id) FROM users;"
            result_last_insert_id = get_one_row(cursor, get_last_insert_id_operation)[INSERT_ID]
            print(result_last_insert_id)
            insert_operation = "INSERT INTO users (user_username, user_password) \
                                            VALUES ('%s', '%s')" % \
                               (username, password)
            try:
                cursor.execute(insert_operation)
                db.commit()
            except:
                db.rollback()
            user_id = result_last_insert_id + 1
            ret = {'user_id': result_last_insert_id + 1}
            return 200, json.dumps(ret)
        # log in
        else:
            # valid password
            if password == result[USERS_USER_PASSWORD]:
                user_id = result[USERS_USER_ID]
                ret = {'user_id': result[USERS_USER_ID]}
                return 200, json.dumps(ret)
            # invalid password: user_id == -1
            else:
                ret = {'user_id': user_id}
                return 200, json.dumps(ret)

    return redirect(url_for('/error'))

@app.route('/wrong_password', methods=['POST', 'GET'])
def wrong_password():
    # TODO: wrong password handler
    return 0

@app.route('/home/<user_id>')
def home_user_id(user_id):
    cursor = db.cursor()

    check_operation = "SELECT * FROM users WHERE user_id = '%s'" % user_id
    result = get_all_row(cursor, check_operation)

    user_plans = []
    plan_dict = {
        "plan_id": 0,
        "start_time": 0,
        "end_time": 0,
        "plan_name": "name"
    }

    for row in result:
        plan_dict["plan_id"] = row[USER_PLAN_PLAN_ID]
        plan_dict["plan_name"] = row[USER_PLAN_PLAN_NAME]
        plan_dict["start_time"] = row[USER_PLAN_START_TIME]
        plan_dict["end_time"] = row[USER_PLAN_END_TIME]
        user_plans.append(plan_dict)

    res = json.dumps(user_plans)

    return 200, res

@app.route('/home/plan_setting/<user_id>', methods=['POST', 'GET'])
def home_plan_setting(user_id):
    # insert into user_plan
    cursor = db.cursor()
    if request.method == 'POST':
        data = request.data
        j_data = json.loads(data)
        start_time = j_data['start_time']
        end_time = j_data['end_time']
        plan_name = j_data['plan_name']

        insert_plan_operation = "INSERT INTO user_plan \
                                    VALUES ('%s', '%s', '%s')" % \
                                    (start_time, end_time, plan_name)
        try:
            cursor.execute(insert_plan_operation)
            db.commit()
        except:
            db.rollback()
            return 404, 'Plan set error'

    return 200, 'Plan set successfully'

# TODO: get users' app usage history automatically

@app.route('/error')
def error():
    return 404, 'Error'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)