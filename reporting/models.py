from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric, Boolean
from .database import Base

class User(Base):
    __tablename__ = "accounts_user"  
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Farm(Base):
    __tablename__ = "farms_farm"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    location = Column(String(300))
    agent_id = Column(Integer, ForeignKey("accounts_user.id"))
    established_date = Column(DateTime, nullable=True)
    area_hectares = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey("accounts_user.id"))

class Farmer(Base):
    __tablename__ = "farms_farmer"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("accounts_user.id"))
    farm_id = Column(Integer, ForeignKey("farms_farm.id"))
    phone = Column(String(20))
    address = Column(String(300))
    is_active = Column(Boolean, default=True)
    created_by_id = Column(Integer, ForeignKey("accounts_user.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Cow(Base):
    __tablename__ = "livestock_cow"
    id = Column(Integer, primary_key=True, index=True)
    cow_tag = Column(String(50), unique=True)
    name = Column(String(100), nullable=True)
    breed = Column(String(20), default='LOCAL')
    birth_date = Column(DateTime, nullable=True)
    gender = Column(String(10), default='Female')
    description = Column(String(300), nullable=True)
    farm_id = Column(Integer, ForeignKey("farms_farm.id"))
    farmer_id = Column(Integer, ForeignKey("farms_farmer.id"), nullable=True)
    weight_kg = Column(Numeric(6, 2), nullable=True)
    color = Column(String(50), nullable=True)
    mother_tag = Column(String(50), nullable=True)
    source = Column(String(10), default='born')
    purchase_date = Column(DateTime, nullable=True)
    purchase_price = Column(Numeric(10,2), default=0)
    is_sold = Column(Boolean, default=False)
    sold_price = Column(Numeric(10,2), nullable=True)
    sold_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class CowActivity(Base):
    __tablename__ = "livestock_cowactivity"
    id = Column(Integer, primary_key=True, index=True)
    cow_id = Column(Integer, ForeignKey("farms_cow.id"))
    activity_type = Column(String(50))
    date = Column(DateTime, nullable=True)
    cost = Column(Numeric(10,2), nullable=True)
    recorded_by_id = Column(Integer, ForeignKey("farms_farmer.id"))
    is_completed = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class MilkProduction(Base):
    __tablename__ = "production_milkproduction"
    id = Column(Integer, primary_key=True, index=True)
    cow_id = Column(Integer, ForeignKey("farms_cow.id"))
    farmer_id = Column(Integer, ForeignKey("farms_farmer.id"))
    farm_id = Column(Integer, ForeignKey("farms_farm.id"))
    date = Column(Date)
    morning_yield_liters = Column(Numeric(6, 2), default=0)
    evening_yield_liters = Column(Numeric(6, 2), default=0)
    total_yield_liters = Column(Numeric(6, 2), default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

