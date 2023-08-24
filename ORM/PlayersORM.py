from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ORM.GamesORM import Game
from ORM.session import get_session
from _log import log

Base = declarative_base()
url = 'postgresql://test:test@localhost/testdb'

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    level = Column(Integer)
    points = Column(Integer)
    tag = Column(String)

    @staticmethod
    def insert(nam, tag):
        """Добавляем игрока в players"""
        session = get_session()
        new_player = Player(name=nam, tag=tag)
        session.add(new_player)
        session.commit()
        log("Player added")

    @staticmethod
    def select(res_id):
        session = get_session()
        player = session.query(Player).get(res_id)
        return player

    @staticmethod
    def select_players():
        """Селект всех игроков"""
        session = get_session()
        players = session.query(Player).all()
        return players

    @staticmethod
    def select_all():
        """Селект для вывода результатов"""
        session = get_session()
        level = Player.level
        points = Player.points
        players = session.query(Player).filter(level.isnot(None)).order_by(level.desc(), points.desc()).all()
        return players

    @staticmethod
    def select_tags():
        session = get_session()
        results = session.query(Player.tag).distinct().all()
        return results

    @staticmethod
    def update(tag, points, level):
        session = get_session()
        session.query(Player).filter(Player.tag == tag).update({'level': level, 'points': points})
        session.commit()

        # result = session.query(Player).filter(Player.tag == tag).first()
        # result.level = level
        # result.points = points
        #
        # session.commit()

    def delete(self):
        session = get_session()
        session.delete(self)
        session.commit()

    def update_players(self, player, result):
        players = player.select_players()

        for p in players:
            points = []
            levels = []
            try:
                res = result.select_player(p.tag)
                for r in res:
                    points.append(r.points)
                    levels.append(r.level)
                points_avg = sum(points) / len(points)
                level_avg = sum(levels) / len(levels)
                player.update(p.tag, points_avg, level_avg)
            except:
                log("Error")