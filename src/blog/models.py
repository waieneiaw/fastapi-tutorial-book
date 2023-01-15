from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    # 特定のUserが投稿したすべてのBlog情報を受け取る
    blogs = relationship("Blog", back_populates="creator")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    # Userクラスのid絡むを外部キーとして指定する
    user_id = Column(Integer, ForeignKey("users.id"))

    # 特定のBlogを投稿したUser情報を受け取る
    creator = relationship("User", back_populates="blogs")
