"""Create database and insert data from the API."""

from sqlalchemy import Column, ForeignKey, Integer, String, Table, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from . import engine

Base = declarative_base()

############## Association tables ##############

product_category_table = Table(
    "product_category",
    Base.metadata,
    Column("product_id", BigInteger, ForeignKey("product.id")),
    Column("category_id", Integer, ForeignKey("category.id")),
)
product_store_table = Table(
    "product_store",
    Base.metadata,
    Column("product_id", BigInteger, ForeignKey("product.id")),
    Column("store_id", Integer, ForeignKey("store.id")),
)

################################################


class Product(Base):
    """Store data for products, nutriscore and url."""

    __tablename__ = "product"
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    product_name = Column(String(100))
    nutriscore_grade = Column(String(20))
    url = Column(String(255))

    categories = relationship(
        "Category", secondary=product_category_table, back_populates="products"
    )

    stores = relationship(
        "Store", secondary=product_store_table, back_populates="products"
    )

    def __repr__(self):
        """Render Product object in a readable way."""
        return f"{self.product_name}"


class Store(Base):
    """Store data for the store related to a product."""

    __tablename__ = "store"
    id = Column(Integer, primary_key=True)
    store_name = Column(String(80), unique=True)

    products = relationship(
        "Product", secondary=product_store_table, back_populates="stores"
    )

    def __repr__(self):
        """Render Store object in a readable way."""
        return f"{self.store_name}"


class Category(Base):
    """Store data for the category related to a product."""

    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    category_name = Column(String(400), unique=True)

    products = relationship(
        "Product", secondary=product_category_table, back_populates="categories"
    )

    def __repr__(self):
        """Render Category object in a readable way."""
        return f"{self.category_name}"


class Favorite(Base):
    """Store data for favorite products."""

    __tablename__ = "favorite"

    id = Column(Integer, primary_key=True)
    product_origin = Column(String(400))
    product_sub = Column(String(400))

    def __repr__(self):
        """Render favorite object in a readable way."""
        return f"{self.product_sub}"


Base.metadata.create_all(engine)
