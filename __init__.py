from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.core.adaptor.DbAdaptor import DbAdaptor
from app.core.module_class import TableModule, ApiModule
from app.modules.url_shortener import urls_crud
from app.modules.url_shortener.table import UrlShortenerTable


class UrlShortener(ApiModule, TableModule):
    def _register_api_bp(self, bp: APIRouter):

        # テーブル関連
        @bp.post('/create', description='create data to table')
        def create(request: Request, dba: DbAdaptor = Depends(DbAdaptor(UrlShortenerTable).dba),
                   target_url: str = Body(..., embed=True)):
            """create a new url shortening"""
            rt = urls_crud.random_create(dba, target_url)
            # リンクの前に付く文字列を作成
            prefix = f'{request.base_url.scheme}://{request.base_url.netloc}'
            rt['short_url'] = f'{prefix}/{rt["link"]}'
            return rt

        @bp.delete('/delete', description='IDかリンクかでデータを削除する')
        def delete(id: Optional[int] = None, link: Optional[str] = None,
                   dba: DbAdaptor = Depends(DbAdaptor(UrlShortenerTable).dba)):
            if id is not None:
                dba.delete(id)
                return {'count': 1}
            if link is not None:
                return dba.delete_by(link=link)
            raise HTTPException(422, 'you cannot input None with twice.')

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
