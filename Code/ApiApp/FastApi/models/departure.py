from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class Departure(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    Id: int
    TrainNumber: str
    Origin: str
    Destination: str
    DepartureTime: datetime
    ArrivalTime: datetime
    Platform: Optional[int] = None
    Status: str
    DelayMinutes: Optional[int] = None
