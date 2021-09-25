from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from app.core.table_class import DateCreateUpdateTable


# see https://fastapi.tiangolo.com/tutorial/sql-databases/
class UrlShortenerTable(DateCreateUpdateTable):
    __tablename__ = 'url_shortener'
    link = Column(String(32), index=True, unique=True)
    target_url = Column(String(2048), index=True)
    enable = Column(Boolean, default=True)
