from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from app.core.table_class import PageTable


# see https://fastapi.tiangolo.com/tutorial/sql-databases/
class SampleTable(PageTable):
    __tablename__ = 'sample'
    data = Column(String(250))
