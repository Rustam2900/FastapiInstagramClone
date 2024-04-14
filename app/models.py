from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.utcnow())


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.utcnow())
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', backref='posts')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    post = relationship('Post', backref='comments')
    owner = relationship('User', backref='comments')


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    post = relationship('Post', backref='likes')
    owner = relationship('User', backref='likes')
