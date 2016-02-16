'''
	Set up catalog database
'''

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Set up 'user' table
class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)

# Set up 'catalog' table
class Catalog(Base):
	__tablename__ = 'catalog'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False, unique=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name': self.name,
			'id': self.id,
		}

# Set up 'catalog_item' table
class CatalogItem(Base):
	__tablename__ = 'catalog_item'
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	catalog_id = Column(Integer, ForeignKey('catalog.id'))
	catalog = relationship(Catalog)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	__table_args__ = (UniqueConstraint('catalog_id', 'name'),)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
		}

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
