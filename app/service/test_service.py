from fastapi import Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger("test_service")


class TestService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def insert():
        logger.info("insert")

    def update():
        logger.info("update")

    def delete():
        logger.info("delete")

    def select():
        logger.info("delete")
