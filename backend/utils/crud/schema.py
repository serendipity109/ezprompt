from pydantic import BaseModel
from typing import Optional, List


class MJImg(BaseModel):
    user_id: str
    prompt: str = ""
    source_url: Optional[str] = None
    size: Optional[str] = "1:1"
    images: List[str]
