from pydantic import BaseModel, ValidationError, validator
from fastapi import Path
import re

class inputText(BaseModel):
    inpText: str #= Path(...)

    @validator('inpText')
    def input_must_str(cls, v):
        if v.isnumeric() == True or re.sub(r"\s+","",v) == "\"\"":
            raise ValidationError("Input must be string and not null")
        return str(v)