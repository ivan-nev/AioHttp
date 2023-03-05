
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, JSON, func, DateTime, ForeignKey
from config_io import PG_DSN





#PG_DSN = 'postgresql+asyncpg://app:secret@127.0.0.1:5431/app'
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    # advertisements = relationship('Advertisement', backref='user', cascade="all, delete")




class Advertisement(Base):

    __tablename__ = 'adv'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    id_user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User', lazy="joined", backref='advertisements')