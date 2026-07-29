from pydantic import BaseModel


class LoadModelRequest(BaseModel):

    model_name: str