from pydantic import BaseModel
from fastapi import Form

class Category(BaseModel):
    name: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
    ) -> 'Category':
        return cls(name=name)
    
