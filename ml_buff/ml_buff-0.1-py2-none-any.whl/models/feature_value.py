import sqlalchemy
from datetime import datetime
from ml_buff.database import DeclarativeBase
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

class FeatureValue(DeclarativeBase):
  __tablename__ = 'feature_values'

  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  value = sqlalchemy.Column(ARRAY(sqlalchemy.Float))
  feature_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('features.id'))
  feature = relationship("Feature")
  input_data_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('input_data.id'))
  input_data = relationship("InputData")
  created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
  updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now, onupdate=datetime.now)


  def __init__(self, value, feature, input_data):
    self.value = value
    self.feature = feature
    self.input_data = input_data
