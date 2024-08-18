from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class UserWardrobe(Base):
    __tablename__ = 'user_wardrobe'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    item_type = Column(String)
    color = Column(String)
    percentage = Column(Float)

class UserSkinTone(Base):
    __tablename__ = 'user_skin_tone'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    skin_tone = Column(String)

engine = create_engine('sqlite:///color_stylist.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)