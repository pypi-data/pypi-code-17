from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from verktyg.utils import cached_property


class SQLAlchemyApplicationMixin(object):
    @property
    def db_url(self):
        return self.config['verktyg_sqlalchemy.database_url']

    @cached_property
    def db_engine(self):
        return create_engine(self.db_url)

    def db_make_session(self):
        return Session(bind=self.db_engine, expire_on_commit=False)

    @contextmanager
    def db_session(self):
        session = self.db_make_session()

        try:
            yield session
            session.commit()
            session.expunge_all()
        except:  # noqa:
            session.rollback()
            raise
        finally:
            session.close()


class SQLAlchemyRequestMixin(object):
    @cached_property
    def db_session(self):
        session = self.app.db_make_session()

        def _close_session():
            try:
                session.rollback()
            finally:
                session.close()

        self.call_on_close(_close_session)
        return session


def bind(builder, *, database_url):
    builder.config['verktyg_sqlalchemy.database_url'] = database_url

    builder.add_application_mixins(SQLAlchemyApplicationMixin)
    builder.add_request_mixins(SQLAlchemyRequestMixin)


__all__ = ['SQLAlchemyApplicationMixin', 'SQLAlchemyRequestMixin']
