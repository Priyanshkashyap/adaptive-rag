"""
Upload response models.
"""

from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel): # basemodel is used to basically describing schema/dto for req,res, or anything
    """
    Response returned after a document upload.

    Attributes:
        status: Whether the upload succeeded.
        filename: Original uploaded filename.
        temp_path: Temporary file path where the upload was saved.
        description: Description provided by the user.
    """

    status: bool = Field(..., description="Whether the upload succeeded.") # field is used to provide extra info about a pydantic field.The ... specifically means:"This field is required and has no default value."
    filename: str = Field(..., description="Original uploaded filename.")
    temp_path: str = Field(..., description="Temporary saved file path.")
    description: str = Field(..., description="User-provided description.")
    chunk_count: int = Field(..., description="chunk count.")