import re
from pydantic import BaseModel, field_validator
from app.exc.email import BadEmail

class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str

    @field_validator("email")
    def validate_email(cls, attr):
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", attr):
            raise BadEmail()
        return attr