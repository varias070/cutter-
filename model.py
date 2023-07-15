from depot.fields.sqlalchemy import UploadedFileField
from sqlalchemy import Column, Integer, String


class Image:
    __tablename__ = 'image'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    content = Column(UploadedFileField)
    carved_content = Column(UploadedFileField)
