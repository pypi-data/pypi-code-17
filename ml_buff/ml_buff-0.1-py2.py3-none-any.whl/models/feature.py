import sqlalchemy
from datetime import datetime
from ml_buff.database import DeclarativeBase
from ml_buff.models import feature_value
from sqlalchemy.orm import relationship

class Feature(DeclarativeBase):
  __tablename__ = 'features'

  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  name = sqlalchemy.Column(sqlalchemy.String)
  feature_values = relationship("FeatureValue", back_populates="feature", cascade="expunge")
  created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
  updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now, onupdate=datetime.now)

  def __init__(self, name):
    self.name = name
