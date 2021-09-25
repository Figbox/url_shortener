import random
import string
from typing import Optional

from app.core.database_engine.DbAdaptor import DbAdaptor
from app.modules.url_shortener.table import UrlShortenerTable


def random_create(dba: DbAdaptor, target_url: str, link_len: int = 5):
    """ランダムにショットリンクを与える"""
    # ランダムにストリング型を生成する
    random_str = ''.join(random.sample(string.ascii_letters, link_len))
    data = UrlShortenerTable(link=random_str,
                             target_url=target_url)
    return dba.add(data)


def get_target_url(dba: DbAdaptor, link: str) -> Optional[str]:
    data: UrlShortenerTable = dba.read_by(link=link)
    print(data.enable)
    if data is None:
        return None
    return data.target_url
