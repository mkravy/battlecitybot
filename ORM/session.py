# Создаем соединение с базой данных
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session():
    # Для posgtres
    # engine = create_engine(url, connect_args={'options': '-csearch_path=bcity'})

    engine = create_engine(f"sqlite:///bcity.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session