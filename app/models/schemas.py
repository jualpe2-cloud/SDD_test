from pydantic import BaseModel

class AuthRequest(BaseModel):
    code: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class RouteBase(BaseModel):
    name: str
    description: str

class RouteDetail(RouteBase):
    distance: float
    duration: int

class PaginationInfo(BaseModel):
    total: int
    page: int
    page_size: int

class RouteListResponse(BaseModel):
    routes: list[RouteDetail]
    pagination: PaginationInfo

class ErrorResponse(BaseModel):
    detail: str
