#!/usr/bin/python
#coding=utf-8

"""
Flask测试用例编写

文档：
http://flask.pocoo.org/docs/0.11/testing/
http://docs.jinkan.org/docs/flask/testing.html
"""


import os
from flask_news import app, db, url_for
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SERVER_NAME'] = 'example.com'
        # app.config['SERVER_NAME'] = 'http://127.0.0.1:5000'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'test.db')
        self.client = app.test_client()
        db.create_all()
        print('testing started.')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        print('testing end.')

    def test_db(self):
        """ 测试数据库 """
        from flask_news import News
        new1 = News(title="标题", content="内容", news_type="百家")
        db.session.add(new1)
        db.session.commit()
        assert new1.id is not None

    def test_index(self):
        """ 测试首页 """
        with app.app_context():
            url = url_for('index')
            rv = self.client.get(url)
        assert '推荐' in rv.get_data(as_text=True)

    def test_add_news(self):
        """ 测试新增新闻 """
        with app.app_context():
            url = url_for('add')
            # 往数据库写入数据，写入成功后，会跳转到首页
            rv = self.client.post(url, data={
                'title': "Bt", 'content': "Nr", 'news_type': "百家"
            })
            # 所以，需要重新请求首页，然后读取首页的内容
            rv = self.client.get(url_for('admin'))
            assert 'Bt' in rv.get_data(as_text=True)

if __name__ == '__main__':
    unittest.main()