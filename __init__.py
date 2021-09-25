import random

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.core.database_engine.DbAdaptor import DbAdaptor
from app.core.module_class import TableModule, ApiModule
from app.core.page_engine.PageAdaptor import PageAdaptor
from app.core.database_engine.db_core import get_db
from app.modules.sample.table import SampleTable
from app.modules.url_shortener import urls_crud
from app.modules.url_shortener.table import UrlShortenerTable


class UrlShortener(ApiModule, TableModule):
    def _register_api_bp(self, bp: APIRouter):
        @bp.post('/show_body')
        def show_body(body: str = Body(..., embed=True)):
            return f'your body is: {body}'

        # テーブル関連
        @bp.post('/create', description='create data to table')
        def create(dba: DbAdaptor = Depends(DbAdaptor(UrlShortenerTable).dba),
                   target_url: str = Body(..., embed=True)):
            """create a new url shortening"""
            return urls_crud.random_create(dba, target_url)

        @bp.delete('/delete', description='delete a data')
        def delete(id: int, dba: DbAdaptor = Depends(DbAdaptor(UrlShortenerTable).dba)):
            return dba.delete(id)

        # 任意なプレフィックスを作成する為
        main_bp = self._register_free_prefix('', 'main')

        @main_bp.get('/{link}', description='you used a free prefix')
        def abc_sample(link: str,
                       dba: DbAdaptor = Depends(DbAdaptor(UrlShortenerTable).dba)):
            return RedirectResponse(urls_crud.get_target_url(dba, link))

    def get_table(self) -> list:
        return [UrlShortenerTable]

    def _get_tag(self) -> str:
        return '短縮URL'

    def get_module_name(self) -> str:
        return 'url_shortener'


url_shortener = UrlShortener()
