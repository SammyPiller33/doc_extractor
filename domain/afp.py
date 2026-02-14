from pydantic import BaseModel, Field
from typing import List, Optional, Any


class Page(BaseModel):
    """Représente une page AFP (BPG)."""

    type: str = Field(default="BPG", description="Type de structured field")
    name: str = Field(default=None, description="Nom de la page")
    bac_papier: str = Field(default="NA", description="Valeur de IMM pour sélection bac papier")
    tle: Optional[list] = Field(default=[], description="Tle spécifiques à la page")
    nop: Optional[list] = Field(default=[], description="Nop spécifiques de la page")

    def add_tle(self, tle: dict[str, str]) -> None:
        """Ajoute un TLE à la page."""
        self.tle.append(tle)

    def add_nop(self, nop: dict[str, str]) -> None:
        """Ajoute un NOP au document."""
        self.nop.append(nop)


    class Config:
        # Pour une sérialisation optimale avec orjson
        json_encoders = {
            bytes: lambda v: v.hex()  # Si tu as des bytes
        }


class Document(BaseModel):
    """Représente un groupe de pages (i.e. BNG) dans un fichier AFP."""

    type: str = Field(default="BNG", description="Type de structured field")
    name: str = Field(default=None, description="Nom du document")
    pages: List[Page] = Field(default_factory=list, description="Liste des pages du document")
    tle: Optional[list] = Field(default=[], description="Tle spécifiques au document")
    nop: Optional[list] = Field(default=[], description="Nop spécifiques à la page")

    def add_page(self, page: Page) -> None:
        """Ajoute une page au document."""
        self.pages.append(page)

    def add_tle(self, tle: dict[str, str]) -> None:
        """Ajoute un TLE au document."""
        self.tle.append(tle)

    def add_nop(self, nop: dict[str, str]) -> None:
        """Ajoute un NOP au document."""
        self.nop.append(nop)

    class Config:
        json_encoders = {
            bytes: lambda v: v.hex()
        }


class Afp(BaseModel):
    """Représente un fichier Afp."""

    type: str = Field(default="BPF", description="Structure parent de l'afp")
    name: str = Field(default=None, description="Nom du document")
    nop: Optional[list] = Field(default=[], description="Nop spécifiques à l'afp")

    def add_nop(self, nop: dict[str, str]) -> None:
        """Ajoute un NOP au document."""
        self.nop.append(nop)

    class Config:
        json_encoders = {
            bytes: lambda v: v.hex()
        }

