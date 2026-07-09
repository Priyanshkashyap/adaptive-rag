"""
Query route classification model.
"""

from typing import Literal
from pydantic import BaseModel

class RouteIdentifier(BaseModel):
    """
    Query route classification result.
    """
    route: Literal[
        "INDEX",
        "GENERAL",
        "SEARCH",
    ]