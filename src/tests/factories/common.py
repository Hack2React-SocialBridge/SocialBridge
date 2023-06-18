from sqlalchemy.orm import scoped_session, sessionmaker
from social_bridge.database import engine

FactoriesSession = scoped_session(sessionmaker(autoflush=False, bind=engine))
