from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str
    # this will later be replaced by hashed password
    password: str
