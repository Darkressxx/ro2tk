import os, sys

from sqlalchemy import Column, Sequence, ForeignKey
from sqlalchemy import Boolean, SmallInteger, Integer, BigInteger, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ItemInfo(Base):
	__tablename__ = "ItemInfo"

	item_id = Column(Integer, unique=True, index=True, primary_key=True)
	item_type = Column(Integer)
	item_type_option = Column(Integer)
	item_category = Column(Integer)
	grade = Column(Integer)
	price_buy = Column(Integer)
	price_sell = Column(Integer)
	stack = Column(Integer)
	item_lv = Column(Integer)
	require_lv = Column(Integer)
	mastery_grade = Column(Integer)
	mastery_lv = Column(Integer)
	require_job = Column(Integer)
	equip_type = Column(Integer)
	equip_slot = Column(Integer)
	weapon_id = Column(Integer)
	armor_id = Column(Integer)
	bind_type = Column(Integer)
	randomset_id = Column(Integer, unique=True)
	socket_group_id = Column(Integer)
	effect_id = Column(Integer)
	skill_id = Column(Integer)
	theme_id = Column(Integer)
	is_drop = Column(Boolean)
	is_deposit = Column(Boolean)
	is_destruct = Column(Boolean)
	is_sell = Column(Boolean)
	is_trade = Column(Boolean)
	is_compose = Column(Boolean)
	category_high = Column(Integer)
	category_medium = Column(Integer)
	category_low = Column(Integer)
	name = Column(String(256))
	name_id = Column(Integer)
	desc = Column(String(4096))
	desc_id = Column(Integer)
	icon = Column(String(256))

class RandomSet(Base):
	__tablename__ = "RandomSet"

	pk = Column(Integer, Sequence("randomset_pk_seq"), primary_key=True)
	randomset = Column(Integer, ForeignKey("ItemSet.randomset_id"))
	item = Column(Integer, ForeignKey("ItemSet.item_id"))
	ratio = Column(Float)
