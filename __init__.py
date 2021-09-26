from fastapi import APIRouter, Body, Depends
from starlette.responses import RedirectResponse

from app.core.database_engine.DbAdaptor import DbAdaptor
from app.core.module_class import TableModule, ApiModule
from app.modules.url_shortener import urls_crud
from app.modules.url_shortener.table import UrlShortenerTable


class UrlShortener(ApiModule, TableModule):
    def _register_api_bp(self, bp: APIRouter):
        # テーブル関連
        @bp.post('/create', description='create data to table')
        def create(dba: DbAdaptor = Depends(DbAdaptor(UrlShortenerTable).dba),
                   target_url: str = Body(..., embed=True)):
            """create a new url shortening"""
            return urls_crud.random_create(dba, target_url)

        # @bp.delete('/delete', description='delete a data')
        # def delete(id: int, dba: DbAdaptor = Depends(DbAdaptor(UrlShortenerTable).dba)):
        #     ...

        # 一番短いのプレフィックスのは何もないこと↓
        main_bp = self._register_free_prefix('', 'main')

        @main_bp.get('/{link}', description='リダイレクト機能を入れている')
        def abc_sample(link: str,
                       dba: DbAdaptor = Depends(DbAdaptor(UrlShortenerTable).dba)):
            target_url = urls_crud.get_target_url(dba, link)
            # ターゲットURLにリダイレクトする
            return RedirectResponse(target_url, status_code=307)

    def get_table(self) -> list:
        return [UrlShortenerTable]

    def _get_tag(self) -> str:
        return '短縮URL'

    def get_module_name(self) -> str:
        return 'url_shortener'


url_shortener = UrlShortener()
