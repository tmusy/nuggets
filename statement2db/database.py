from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('mysql://state_man:2db-stM14@localhost/statement2db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import statement2db.model
    Base.metadata.create_all(bind=engine)


def clear_db():
    db_session.close()
    Base.metadata.drop_all(bind=engine)
