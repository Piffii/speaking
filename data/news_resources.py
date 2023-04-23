from flask import jsonify, Flask
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.cosmo_news import Cosmo_News
from data.reqparse import parser


app = Flask(__name__)
api = Api(app)


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(Cosmo_News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(Cosmo_News).get(news_id)
        return jsonify({'news': news.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(Cosmo_News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Cosmo_News).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = Cosmo_News(
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})
