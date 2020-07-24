from fs.info import Info
from pydantic import BaseModel


class EntryInfo(BaseModel):
    name: str
    size: int
    type: int

    @classmethod
    def from_storage(cls, info: Info):
        return cls(
            name=info.name,
            size=info.size,
            type=info.type,
        )
