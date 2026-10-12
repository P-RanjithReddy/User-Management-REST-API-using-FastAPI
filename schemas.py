from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=18, le=60)
    city: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True

    @field_validator("name", "city")
    @classmethod
    def trim_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field is required")
        return value

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=18, le=60)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None

    @field_validator("name", "city")
    @classmethod
    def trim_optional_text(cls, value):
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("This field cannot be blank")
        return value

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int
    city: str
    is_active: bool
