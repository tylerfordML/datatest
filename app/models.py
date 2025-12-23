from pydantic import BaseModel, Field
from typing import List


class RomanNumeralResponse(BaseModel):
    """
    Response model for single integer conversion.
    """
    input: str = Field(..., json_schema_extra={"example" : "10"})
    output: str = Field(..., json_schema_extra={"example" : "X"})


class RomanNumeralItem(BaseModel):
    """
    Represents a single conversion within a range.
    """
    input: str = Field(..., json_schema_extra={"example" : "4"})
    output: str = Field(..., json_schema_extra={"example" : "IV"})


class RomanNumeralRangeResponse(BaseModel):
    """
    Response model for range conversions.
    """
    conversions: List[RomanNumeralItem]


class ErrorResponse(BaseModel):
    """
    Standard error response model.
    """
    detail: str = Field(..., json_schema_extra={"example" : "Input must be between 1 and 255"})
