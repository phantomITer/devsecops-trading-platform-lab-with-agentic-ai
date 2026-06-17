
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    account_id: int
    symbol: str
    quantity: float
    avg_price: float
    updated_at: datetime
