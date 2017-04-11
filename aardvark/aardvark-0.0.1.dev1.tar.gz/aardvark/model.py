from aardvark import db
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
# DateTime, Boolean, Unicode, Text


class AWSIAMObject(db.Model):
    """
    Meant to model AWS IAM Object Access Advisor.
    """
    __tablename__ = "aws_iam_object"
    id = Column(Integer, primary_key=True)
    arn = Column(Text(), nullable=True, index=True, unique=True)
    usage = relationship("AdvisorData", backref="item", cascade="all, delete, delete-orphan", foreign_keys="AdvisorData.item_id")

    @staticmethod
    def get_or_create(arn):
        item = AWSIAMObject.query.filter(AWSIAMObject.arn==arn).scalar()
        if not item:
            item = AWSIAMObject(arn=arn)
            db.session.add(item)
            db.session.commit()
            db.session.refresh(item)
        return item


class AdvisorData(db.Model):
    """
    Models certain IAM Access Advisor Data fields.

    {
      "totalAuthenticatedEntities": 1,
      "lastAuthenticatedEntity": "arn:aws:iam::XXXXXXXX:role/name",
      "serviceName": "Amazon Simple Systems Manager",
      "lastAuthenticated": 1489176000000,
      "serviceNamespace": "ssm"
    }
    """
    __tablename__ = "advisor_data"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("aws_iam_object.id"), nullable=False, index=True)
    lastAuthenticated = Column(Integer)
    serviceName = Column(String(128), index=True)
    serviceNamespace = Column(String(64), index=True)

    @staticmethod
    def create_or_update(item_id, lastAuthenticated, serviceNae, serviceNamespace):
        item = AdvisorData.query.filter(AdvisorData.item_id==item_id) \
            .filter(AdvisorData.serviceNamespace==serviceNamespace).scalar()

        if not item:
            item = AdvisorData(item_id=item_id, 
                               lastAuthenticated=lastAuthenticated,
                               serviceName=serviceNae,
                               serviceNamespace=serviceNamespace)
            db.session.add(item)
            db.session.commit()
            return

        if lastAuthenticated > item.lastAuthenticated:
            item.lastAuthenticated = lastAuthenticated
            db.session.add(item)
            db.session.commit()
