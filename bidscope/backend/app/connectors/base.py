from typing import Protocol
from app.domain.schemas import QueryIntent, Notice, SourceHealth

class SourceConnector(Protocol):
    source_id: str
    async def healthcheck(self) -> SourceHealth: ...
    async def search(self, intent: QueryIntent) -> list[Notice]: ...
