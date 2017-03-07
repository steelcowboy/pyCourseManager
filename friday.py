import json, os
from datetime import datetime 

from course_manager import CourseManager

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)
CORS(app)

db = SQLAlchemy(app)

app.config.update(
    SQLALCHEMY_DATABASE_URI = 'sqlite:////srv/pyflowchart/users.db',
    SQLALCHEMY_TRACK_MODIFICATIONS = True,
    SECRET_KEY = 'secret_xxx'
)

# courses = {}
# last_course_ids = {}

today = datetime.today()

fall = datetime(today.year, 9, 15)
winter = datetime(today.year, 1, 1)
spring = datetime(today.year, 3, 31)
summer = datetime(today.year, 6, 15)

if fall <= today <= datetime(today.year, 12, 31):
    quarter = 0
elif winter <= today < spring:
    quarter = 1
elif spring <= today < summer:
    quarter = 2
else:
    quarter = 3

# This should be read from a config file
# course_root = "/srv/pyflowchart/"

# users = {}

# class User(UserMixin):
    # def __init__(self, username, pw):
        # self.id = username
        # self.username = username
        # self.password = pw 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

# /login/username
# class LoginResource(Resource):
    # def post(self, username):
        # if username not in users:
            # abort(404, message=f"User {username} does not exist")

        # print(request.headers)
        # api_key = request.headers.get('x-api-key')
        # if not api_key:
            # abort(401, message=f"Please provide password for {username} in the 'api-key' header")


        # user = users[username]
        # if user.password == api_key:
            # login_user(user)
        # else:
            # abort(401, message=f"Password incorrect for {username}")

# /sign_up/username 
# class NewUserResource(Resource):
    # def post(self, username):
        # global users

        # if username in users:
            # abort(409, message=f"User {username} already exists")

        # print(request.headers)
        # api_key = request.headers.get('x-api-key')
        # if not api_key:
            # abort(401, message=f"Please provide password for {username} in the 'api-key' header")
        
        # users[username] = User(username, api_key)

# /logout
# class LogoutResource(Resource):
    # @login_required
    # def get(self):
        # logout_user()

# Login resources
# api.add_resource(LoginResource,   '/login/<string:username>')
# api.add_resource(NewUserResource, '/new_user/<string:username>')
# api.add_resource(LogoutResource,  '/logout')

api.add_resource(CourseManager.UsageResource,   '/')
api.add_resource(CourseManager.ListStockCharts, '/stock_charts')
api.add_resource(CourseManager.ListUserCharts,  '/<string:user>/charts')
api.add_resource(CourseManager.GetStockChart,   '/stock_charts/<string:major>')
api.add_resource(CourseManager.ChartResource,   '/<string:user>/charts/<string:chart>')
api.add_resource(CourseManager.CourseResource,  '/<string:user>/charts/<string:chart>/<int:c_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6500)

