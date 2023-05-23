from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger, Text, Table

Base = declarative_base()

tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("post_id", BigInteger, ForeignKey("post.id")),
    Column("tag_id", BigInteger, ForeignKey("tag.id"))
)


class Post(Base):
    __tablename__ = "post"
    id = Column(BigInteger, primary_key=True, nullable=False)
    title = Column(String(250), nullable=False, unique=False)
    url = Column(String, unique=True, nullable=False)
    author_id = Column(BigInteger, ForeignKey("author.id"))
    author = relationship("Author", backref="posts")
    tags = relationship("Tag", secondary=tag_post, backref="posts")


class Author(Base):
    __tablename__ = "author"
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(250), nullable=False)
    url = Column(String, unique=True, nullable=False)
    # tag_post = relationship("Tag", secondary=tag_post, backref="posts")


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', backref='comments')
    post_id = Column(Integer, ForeignKey('post.id'))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
