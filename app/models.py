from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import validates
 
db = SQLAlchemy()
 
 
class Hero(db.Model):
    __tablename__ = "heroes"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    super_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
    hero_powers = db.relationship("HeroPower", back_populates="hero")
 
 
class Power(db.Model):
    __tablename__ = "powers"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
    hero_powers = db.relationship("HeroPower", back_populates="power")
 
    @validates("description")
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description
 
 
class HeroPower(db.Model):
    __tablename__ = "hero_powers"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    strength = Column(String)
 
    hero_id = Column(Integer, ForeignKey("heroes.id"), nullable=False)
    power_id = Column(Integer, ForeignKey("powers.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
    hero = db.relationship("Hero", back_populates="hero_powers")
    power = db.relationship("Power", back_populates="hero_powers")
 
    @validates("strength")
    def validate_strength(self, key, strength):
        valid_strengths = ["Strong", "Weak", "Average"]
        if strength not in valid_strengths:
            raise ValueError(f"Strength must be one of: {', '.join(valid_strengths)}")
        return strength