from pydantic import BaseModel


class JobQuery(BaseModel):
    domain: str
    skills: list
    experience: int
    country: str
    city: str
