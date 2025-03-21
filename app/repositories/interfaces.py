from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar

T = TypeVar('T')
S = TypeVar('S')


class StorageInterface(Protocol, Generic[T, S]):

    async def get(self, id: Any) -> Optional[S]: ...
    async def get_all(self) -> Optional[List[S]]: ...
    async def create(self, obj_data: Dict[str, Any]) -> S: ...
    async def remove_roll(self, roll_id: int) -> Optional[S]: ...
    async def get_filtered(self, criteria: Any) -> Optional[List[S]]: ...
    async def get_statistics_data(self, model: Any, period: Any) -> Optional[S]: ...
