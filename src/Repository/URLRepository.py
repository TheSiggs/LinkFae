import secrets
from sqlalchemy.orm import Session
from src.Entity.URL import URL


def get_url(db: Session, url_id: int):
    return db.query(URL).filter(URL.id == url_id).first()


def get_url_by_key(db: Session, key: str):
    url = db.query(URL).filter(URL.key == key, URL.is_active).first()
    if url:
        url.clicks += 1
        db.commit()
        db.refresh(url)
        return url
    return None

def create_url(db: Session, url: str):
    db_url = URL()
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    key = "".join(secrets.choice(chars) for _ in range(10))
    db_url.key = key
    db_url.target_url = url
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
