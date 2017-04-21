import sqlalchemy
from datetime import datetime
from ml_buff.database import DeclarativeBase
from sqlalchemy.orm import relationship

class InputData(DeclarativeBase):
    __tablename__ = 'input_data'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    external_id = sqlalchemy.Column(sqlalchemy.Integer)
    dataset_name = sqlalchemy.Column(sqlalchemy.String)
    feature_values = relationship("FeatureValue", back_populates="input_data")
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, default = datetime.now)

    def __init__(self, external_id, dataset_name):
        self.external_id = external_id
        self.dataset_name = dataset_name
