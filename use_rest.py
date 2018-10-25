#!/usr/bin/python
#coding=utf-8

"""
http://flask-restful.readthedocs.io/en/0.3.5/quickstart.html
http://www.pythondoc.com/Flask-RESTful/reqparse.html
"""
from flask import Flask
from flask_restful import Resource, Api

from flask_news import News

app = Flask(__name__)
api = Api(app)



class HelloWorld(Resource):
    def get(self):
        news_list = News.query.all()
        rest = []
        for new_obj in news_list:
            rest.append({
                'id': new_obj.id,
                'title': new_obj.title
                })
        return rest

    def post(self):
        return {'test': 'test'}

    def put(self):
        return {'put': 'put'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)