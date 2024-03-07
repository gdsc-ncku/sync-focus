from typing import Any, Generator

from sqlalchemy.orm import Session, sessionmaker

from .db import NewSessionMaker
from .setting import Settings, get_settings


class Dependencies:
    session_maker: sessionmaker[Session]
    setting: Settings

    def __init__(self) -> None:
        self.setting = get_settings()
        engine, sessionmaker = NewSessionMaker(self.setting)
        self.session_maker = sessionmaker

    def get_db(self) -> Generator[Session, Any, None]:
        db = self.session_maker()
        try:
            yield db
        finally:
            db.close()


deps = Dependencies()
