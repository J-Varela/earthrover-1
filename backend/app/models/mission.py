from pydantic import BaseModel, FiniteFloat


class Mission(BaseModel):
    target_x: FiniteFloat
    target_y: FiniteFloat
