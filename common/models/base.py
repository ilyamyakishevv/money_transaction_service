from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.sqltypes import ARRAY, String


class Base(DeclarativeBase):
    type_annotation_map = {
        list: ARRAY,
        list[str]: ARRAY(String),
        list[int]: ARRAY(Integer),
    }