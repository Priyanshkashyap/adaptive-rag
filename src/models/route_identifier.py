"""
Query route classification model.
"""

from pydantic import BaseModel


class RouteIdentifier(BaseModel):
    """
    Route classification result.

    Attributes:
        route:
            Query route type.
    """

    route: str
