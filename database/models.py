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
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(250), nullable=False, unique=False)
    url = Column(String, unique=True, nullable=False)
    author_id = Column(BigInteger, ForeignKey("author.id"))
    author = relationship("Author")
    tags = relationship("Tag", secondary=tag_post, backref="posts")


class Author(Base):
    __tablename__ = "author"
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(250), nullable=False)
    url = Column(String, unique=True, nullable=False)
    # tag_post = relationship("Tag", secondary=tag_post, backref="posts")


class Tag(Base):
    __tablename__ = "tag"
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, unique=True, nullable=False)
