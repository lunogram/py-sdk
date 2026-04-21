from typing import TypedDict, NotRequired

class Identifier(TypedDict):
    id: str
    source: str
    external_id: str
    metadata: NotRequired[None]
    created_at: str
    updated_at: str