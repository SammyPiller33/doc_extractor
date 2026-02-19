from pydantic import BaseModel, Field
from typing import List, Optional, Any


class Tle(BaseModel):
    """Represents a Tag Logical Element (TLE)."""

    name: str = Field(description="TLE name (FQN)")
    value: str = Field(default="", description="TLE value (AttrVal)")

    class Config:
        json_encoders = {
            bytes: lambda v: v.hex()
        }

class Page(BaseModel):
    """Represents an afp page (BPG)."""

    page_number: str = Field(default=None, description="Page number")
    bac_papier: str = Field(default="NA", description="IMM value for paper tray selection")
    tle: Optional[list[Tle]] = Field(default=[], description="Page-specific TLEs")
    nop: Optional[list[str]] = Field(default=[], description="Page-specific NOPs")

    def add_tle(self, tle: Tle) -> None:
        """Add a TLE to the page."""
        self.tle.append(tle)

    def add_nop(self, nop: str) -> None:
        """Add a nop to the page."""
        self.nop.append(nop)


    class Config:
        # For optimal serialization with orjson
        json_encoders = {
            bytes: lambda v: v.hex()
        }


class Document(BaseModel):
    """Represents a group of pages (i.e. BNG) in an AFP file."""

    doc_number: str = Field(default=None, description="Document number")
    pages: List[Page] = Field(default_factory=list, description="Document pages list")
    tle: Optional[list[Tle]] = Field(default=[], description="Document-specific TLEs")
    nop: Optional[list[str]] = Field(default=[], description="Document-specific NOPs")

    def add_page(self, page: Page) -> None:
        """Add a file to the document."""
        self.pages.append(page)

    def add_tle(self, tle: Tle) -> None:
        """Add a TLE to the document."""
        self.tle.append(tle)

    def add_nop(self, nop: str) -> None:
        """Add a nop to the document."""
        self.nop.append(nop)

    class Config:
        json_encoders = {
            bytes: lambda v: v.hex()
        }


class Afp(BaseModel):
    """Represents an AFP file."""

    name: str = Field(default=None, description="AFP file name")
    nop: Optional[list[str]] = Field(default=[], description="AFP-specific NOPs")
    nb_of_docs: int = Field(default=0, description="Number of documents in the AFP file")
    nb_of_pages: int = Field(default=0, description="Number of pages in the AFP file")

    def add_nop(self, nop: str) -> None:
        """Add a nop to the document."""
        self.nop.append(nop)

    def set_nb_of_docs(self, nb_of_docs: int) -> None:
        self.nb_of_docs = nb_of_docs

    def set_nb_of_pages(self, nb_of_pages: int) -> None:
        self.nb_of_pages = nb_of_pages

    class Config:
        json_encoders = {
            bytes: lambda v: v.hex()
        }

