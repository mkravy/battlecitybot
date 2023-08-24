from _log import log

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ORM.GamesORM import Game
from ORM.session import get_session

Base = declarative_base()
url = 'postgresql://test:test@localhost/testdb'

class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(Integer)
    points = Column(Integer)
    tag = Column(String)


    @staticmethod
    def insert(tag, level, points):
        session = get_session()
        new_result = Result(level=level, points=points, tag=tag)
        session.add(new_result)
        session.commit()

    @staticmethod
    def select(res_id):
        session = get_session()
        result = session.query(Result).get(res_id)
        return result

    @staticmethod
    def select_all():
        session = get_session()
        results = session.query(Result).all()
        return results

    @staticmethod
    def select_tags():
        session = get_session()
        tags = session.query(Result.tag).distinct().all()
        return tags

    @staticmethod
    def select_player(tag):
        session = get_session()
        player = session.query(Result).filter(Result.tag.ilike(f"%{tag}%")).all()
        return player

    @staticmethod
    def update(tag, points, level):
        session = get_session()
        result = session.query(Result).filter(Result.tag == tag).first()
        result.level = level
        result.points = points

        session.commit()
        # print("Updated succesfully!")

    def delete(self):
        session = get_session()
        session.delete(self)
        session.commit()

    def update_results(self, game, result):
        game_tags = game.select_tags()
        result_tags = result.select_tags()
        rtags = []
        for r in result_tags:
            rtags.append(r[0])

        for t in game_tags:
            tag = t[0]
            points = game.select_max_points(tag)
            level = game.select_max_level(tag)

            if tag not in rtags:
                result.insert(tag, level, points)
            else:
                result.update(tag, points, level)