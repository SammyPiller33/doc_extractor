"""Handlers for parsing SFI components."""

from abc import ABC, abstractmethod
from typing import Any, Optional
from parser.afp.triplet_config import TRIPLET_CONFIG
from parser.afp.triplet_handlers import TRIPLET_HANDLERS


class SfComponentHandler(ABC):
    """Base class for SF component handlers."""

    @abstractmethod
    def parse(self, f, component_length) -> Optional[Any]:
        """
        Parse an SF component from the file stream.

        Args:
            f: File-like object positioned at component start
            component: SfComponent configuration
            context: Parsing context (e.g., parsed values, flags)

        Returns:
            tuple: (field_name, parsed_value) or None to skip
            :param f:
            :param component_length:
        """
        pass

    @staticmethod
    def parse_char(f, component_length) -> Optional[str]:
        return f.read(component_length).decode('cp500', errors='replace').rstrip()


class HexaHandler(SfComponentHandler):
    """Handler for TYPE_RAW (raw bytes as hex)."""

    def parse(self, f, component_length) -> Optional[tuple[str, Any]]:

        if component_length > 1:
            return f.read(component_length).hex().upper()
        else:
            return None


class CharHandler(SfComponentHandler):
    """Handler for TYPE_CHAR (single ASCII character)."""

    def parse(self, f, component_length) -> Optional[tuple[str, Any]]:
        return self.parse_char(f, component_length)


class TripletHandler(SfComponentHandler):
    """Handler for TYPE_TRIPLET (repeating triplet structures)."""

    def parse(self, f, component_length) -> Optional[list[Any]]:

        offset = 0
        triplets = []

        while offset < component_length:

            t_len = f.read(1)[0]
            t_id = f.read(1)[0].to_bytes(1, 'big')
            t_config = TRIPLET_CONFIG.get(t_id, None)

            if not t_config:
                # Triplet inconnu : on lit le contenu brut
                content = (t_len.to_bytes(1, 'big') + t_id + f.read(t_len - 2)).hex().upper()
                triplets.append({
                    "NA": content
                })
            else:
                t_name = t_config.short_name
                t_struct = t_config.struct

                # Dictionnaire pour stocker tous les composants du triplet
                triplet_data = {}

                # Position de lecture relative au début du triplet
                bytes_read = 2  # t_len + t_id déjà lus

                for component in t_struct:
                    handler = TRIPLET_HANDLERS.get(component.type, None)

                    if not handler:
                        continue

                    # Calculer la longueur réelle pour les composants à longueur variable
                    comp_length = component.length
                    if comp_length == 0:
                        # Longueur variable = reste du triplet
                        comp_length = t_len - bytes_read

                    # Parser le composant
                    value = handler.parse(f, comp_length)

                    # Ajouter au dictionnaire seulement si non-None
                    if value is not None:
                        triplet_data[component.name] = value

                    bytes_read += comp_length

                # Ajouter le triplet complet
                triplets.append({
                    t_name: triplet_data
                })

            offset += t_len

        return triplets


# Registry
SF_HANDLERS = {
    1: HexaHandler(),
    2: CharHandler(),
    3: TripletHandler(),
}
