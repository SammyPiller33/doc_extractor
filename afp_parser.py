from pathlib import Path

from file_parser import FileParser
from file_manager import read_file_binary

class AfpParser(FileParser):

    STRUCTURED_FIELDS = {

        # Groupes de ressources / délimiteurs
        "BDT": "D3A8A0",  # Begin Document
        "EDT": "D3A9A0",  # End Document
        "BNG": "D3A8A6",  # Begin Named Group (mailpiece)
        "ENG": "D3A9A6",  # End Named Group
        "BPG": "D3A8A2",  # Begin Page Group
        "EPG": "D3A9A2",  # End Page Group

        # Contrôles
        "IMM": "D3ABA0",  # Invoke Medium Map (changement papier)
        "NOP": "D3A0F8",  # No Operation (commentaires)

        # Métadonnées principales
        "TLE": "D3A8AF",  # Tagged Logical Element

        # Line Data (pour contexte)
        "LND": "D3A6E7",  # Line Descriptor
        "RCD": "D3A68D",  # Record Descriptor
        "IDM": "D3ABCA"  # Invoke Data Map
    }

    CARRIAGE_CONTROL_CHARACTER = "5A"

    FIELD_HEADER = {

    }

    def __init__(self, path: Path):
        super().__init__(path)
        self._raw_data = read_file_binary(self._path)
        self._sf_map = {bytes.fromhex(v): k for k, v in self.STRUCTURED_FIELDS.items()}
        self.offset = 0
        self.length = len(self._raw_data)

    def get_bytes(self) -> bytes:
        return self._raw_data

    def get_hexa(self) -> str:
        return ' '.join(f'{b:02x}' for b in self._raw_data)

    def parse(self) -> dict:
        print("Parsing du fichier AFP")
        print(self._path)
        return {"type": "afp"}

#
# a = AfpParser(Path("./sample/01_Health_Coverage.afp"))
# print(' '.join(f'{b:02x}' for b in a.get_bytes()))

