from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    user_id: UUID
    name: str
    email: str
    password: str
    is_active: bool
    created_at: str
    updated_at: str
    deleted_at: str