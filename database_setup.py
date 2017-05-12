import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Registration(Base):
	__tablename__ = 'registration'

	username = Column(String(80), nullable = False)
	password = Column(String(250), nullable = False)
	id = Column(Integer, primary_key = True)

class Expenses(Base):
	__tablename__ = 'expenses'

	id = Column(Integer, primary_key = True)
	price = Column(Float, nullable = False)
	date = Column(Date, nullable = False)
	description = Column(String(5000))
	user_id = Column(Integer, ForeignKey('registration.id'))

	user = relationship(Registration)

# ending configuration
engine = create_engine('sqlite:///userexpenses.db')

Base.metadata.create_all(engine)