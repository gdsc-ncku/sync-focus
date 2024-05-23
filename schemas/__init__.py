from .heartbeat import *  # noqa
from .user import *  # noqa
from .duration import *  # noqa
from .setting import *  # noqa
from .summary_item import * # noqa
from .summary import *


from pydantic import BaseModel


class DetailSchema(BaseModel):
    detail: str

