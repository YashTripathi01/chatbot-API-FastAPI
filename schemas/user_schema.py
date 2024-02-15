from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator


class UserBase(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    mobile: str = Field(...)


class UserCreate(UserBase):
    name: str = Field(..., pattern=r"^[A-Za-z\s']{1,50}$")
    email: EmailStr = Field(...)
    mobile: str = Field(..., pattern=r"^[0-9]{10}$")

    @validator("mobile")
    def add_country_code(cls, value):
        return f"+91{value}"


class UserUpdate(UserBase):
    name: str = Field(None, pattern=r"^[A-Za-z\s']{1,50}$")
    email: EmailStr = Field(None)
    mobile: str = Field(None, pattern=r"^[0-9]{10}$")

    @validator("mobile")
    def add_country_code(cls, value):
        if value is not None:
            return f"+91{value}"


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(...)
