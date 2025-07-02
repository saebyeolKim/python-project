from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="author") # 사용자가 작성한 게시글들 (1:N 관계의 N)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

    user_id = Column(Integer, ForeignKey("users.id")) # 게시글의 작성자 아이디
    author = relationship("User", back_populates="posts") # 게시글 작성자 (User 객체 참조)