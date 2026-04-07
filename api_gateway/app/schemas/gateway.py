from pydantic import BaseModel, Field


class GatewayErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str
    details: dict = Field(default_factory=dict)


class GatewaySuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: dict = Field(default_factory=dict)
