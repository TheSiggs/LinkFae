import os
import validators
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from src.Database.Database import engine, Base, SessionLocal
from src.Repository import URLRepository
from src.Repository.URLRepository import get_url_by_key
from src.Schema.URL.URLBase import URLBase
from typing import Annotated

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


isDev = os.environ.get("ENV") == "dev"

app = FastAPI(
    docs_url="/docs" if isDev else None,
    redoc_url="/redoc" if isDev else None
)

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/shorten")
def create_url(url: str, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    if token != os.getenv('SECRET_KEY'):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not validators.url(url):
        raise_bad_request(message="Your provided URL is not valid")
    if len(url) > 10000:
        raise_bad_request(message="Your provided URL is not valid")
    url = URLRepository.create_url(db=db, url=url)
    hostname = os.getenv("HOSTNAME")

    return f"{hostname}/{url.key}"


@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):
    url = get_url_by_key(db, url_key)
    if url:
        return RedirectResponse(url.target_url)
    else:
        raise HTTPException(status_code=404, detail=f"URL '{request.url}' doesn't exist")
