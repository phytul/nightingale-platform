from pydantic import BaseModel, Field
from typing import Annotated, Literal


# 在视图函数中，在某些操作，不需要返回具体数据时，我们可以返回一个固定的响应格式。
class ResponseOut(BaseModel):
    result: Annotated[Literal["success", "failure"], Field("success", description="操作结果")]