import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session


class Database:
    def __init__(self):
        db_host = os.environ['DB_HOST']
        db_port = os.environ['DB_PORT']
        db_name = os.environ['DB_NAME']
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASSWORD']

        self.engine = create_engine(
            f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )

        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.session: Session = self.Session()

    def get_table(self, table_name):
        from sqlalchemy import Table
        return Table(table_name, self.metadata, autoload_with=self.engine)

    def execute(self, statement):
        return self.session.execute(statement)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()
