from src.Schema.URL.URLBase import URLBase


class URL(URLBase):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True
