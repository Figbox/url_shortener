import random

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.core.database_engine.DbAdaptor import DbAdaptor
from app.core.module_class import TableModule, ApiModule
from app.core.page_engine.PageAdaptor import PageAdaptor
from app.core.database_engine.db_core import get_db
from app.modules.sample.table import SampleTable


class Sample(ApiModule, TableModule):
    def _register_api_bp(self, bp: APIRouter):
        @bp.get('/description')
        def description():
            return 'this is a sample module_manager description,' \
                   ' this sample will tell you how to' \
                   ' create a module_manager for Figbox'

        @bp.post('/show_body')
        def show_body(body: str = Body(..., embed=True)):
            return f'your body is: {body}'

        # テーブル関連
        @bp.post('/create', description='create data to table')
        def create(dba: DbAdaptor = Depends(DbAdaptor(SampleTable).dba),
                   data: str = Body(..., embed=True)):
            """create data into the table"""
            data = SampleTable(data=data,
                               link=str(random.randint(0, 99999)),
                               title=data,
                               content=data)
            return dba.add(data)

        @bp.get('/read', description='read data from table')
        def read(dba: DbAdaptor = Depends(DbAdaptor(SampleTable).dba)):
            """read data from table"""
            return dba.read_all()

        @bp.put('/update', description='update')
        def update(id: int, dba: DbAdaptor = Depends(DbAdaptor(SampleTable).dba),
                   data: str = Body(..., embed=True)):
            sample_data = dba.read_by_id(id)
            sample_data.data = data
            return dba.update(sample_data)

        @bp.delete('/delete', description='delete a data')
        def delete(id: int, dba: DbAdaptor = Depends(DbAdaptor(SampleTable).dba)):
            return dba.delete(id)

        @bp.get('/page/{link}', description='show a page')
        def show_page(link: str, page_adaptor: PageAdaptor = Depends()):
            return page_adaptor.bind(SampleTable, link, 'sample/temp.html')

        # 任意なプレフィックスを作成する為
        abc_bp = self._register_free_prefix('/abc', 'abc')

        @abc_bp.get('/sample', description='you used a free prefix')
        def abc_sample():
            return 'you used a free prefix'

    def get_table(self) -> list:
        return [SampleTable]

    def _get_tag(self) -> str:
        return 'サンプルモジュール'

    def get_module_name(self) -> str:
        return 'sample'


sample = Sample()
