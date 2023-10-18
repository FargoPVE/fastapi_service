from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    services: List[str]
    quantity: int
    image_id: int


class SRoomInfo(SRoom):
    model_config = ConfigDict(from_attributes=True)

    total_cost: int
    rooms_left: int
