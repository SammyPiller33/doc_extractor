from pathlib import Path
from sf_config import *

class SfStreamer:
    """Class for streaming structured fields from an AFP file."""

    def __init__(self, afp_path: str) -> None:

        # Construct the path to the AFP file
        try:
            self.afp_path = Path(afp_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{afp_path}' does not exist.")
        except Exception as e:
            raise Exception(f"An error occurred when initiating the afp_path : {e}")

        # Initialize the offset and length of the AFP file.
        # The offset is set to 0 and incremented as structured fields are read.
        self.afp_offset = 0
        # The length is obtained from the file size. It is used to determine when to stop reading structured fields.
        self.afp_len = self.afp_path.stat().st_size

    def stream(self):
        """Stream structured fields from the AFP file one at a time (generator)."""

        # Iterate over the AFP structure fields until the end of the file is reached
        while self.afp_offset < self.afp_len:
            try:
                # Open the AFP file in binary mode. It allows reading bytes.
                with open(self.afp_path, "rb") as f:
                    # Read the next structured field and yield it.
                    # The structured field is returned as a dictionary containing its metadata and data.
                    yield self.read_sf(f)

            except FileNotFoundError:
                raise FileNotFoundError(f"Le fichier '{self.afp_path}' n'existe pas.")

            except EOFError:
                raise EOFError("End of file reached.")

            except Exception as e:
                raise Exception(f"Erreur inconnue : {e}")

    def read_sf(self, f) -> dict:
        """Read the next structured field from the file."""

        f.seek(self.afp_offset, 0)

        # Check if the file is an AFP file by reading the first byte of the next chunck.
        # The carriage control byte 0x5A starts each structured field.
        control = f.read(1)
        if control != CARRIAGE_CONTROL:
            raise ValueError("Le fichier n'est pas un fichier AFP conforme")

        # Parse the SFI. It contains information about the structured field type, its length, and other metadata.
        sfi_data = self._parse_sfi(f)

        # Get the structured field type name from the SF ID, in the SF_TYPES dictionary.
        sf_name = SF_TYPES[sfi_data['sf_id']].short_name

        # Parse the SF data. It contains the actual structured field data.
        sf_data = self._parse_sf(f, sfi_data)

        self.afp_offset += sfi_data['sf_len'] + 1
        return {
            'sf_name': sf_name,
            'sfi_data': sfi_data,
            'sf_data': sf_data
        }

    @staticmethod
    def _parse_sfi(f) -> dict:
        """Parse the Structured Field Introducer - common to all structured fields."""
        # Declare a dict to store parsed data
        sfi_parsed = {}

        # Iterate over each component of the SFI. Each component has an offset, a length, a given name,
        # and a boolean indicating whether it is mandatory.
        # Each component is processed according to its type (int, bytes, etc.)
        for component in SFI:

            # Test if the component is mandatory. Mandatory components are parsed without any condition.
            if component.mandatory:

                # Read the component's data. The length is given by the component's attribute.
                # The data is read as bytes.
                data = f.read(component.length)

                # Test if the component is the SF length (sf_len).
                if component.name == 'sf_len':
                    # Cast int from Big-endian (2 bytes). Big-endian byte order = most significant byte first.
                    sfi_parsed[component.name] = int.from_bytes(data, byteorder='big')

                # Test if the component is the SF ID (sf_id). The id is a unique identifier
                # for each structured field type.
                elif component.name == 'sf_id':
                    # Store the SF ID as bytes
                    sfi_parsed[component.name] = data

                # Test if the component is the Flags (flags).
                # The flags field contains control information. The first bit indicates whether an extension is present.
                elif component.name == 'flags':
                    # Extract the single byte value and display as binary
                    sfi_parsed[component.name] = f"{data[0]:08b}"
                    # Check if the extension bit is set
                    sfi_parsed['has_extension'] = bool(data[0] & 0x80)

                # Test if the component is the Reserved (reserved).
                # The reserved field is reserved by the standard for future use. No need to parse it.
                elif component.name == 'reserved':
                    continue

            # Test if the component is not mandatory and if an extension is present.
            # The optional component is parsed only if the extension bit is set in the flags field.
            elif not component.mandatory and sfi_parsed.get('has_extension', False):

                # Test if the component is the Extension Length (extension_len). It is stored as a single byte.
                if component.name == 'extension_len':
                    data = f.read(component.length)
                    ext_len = data[0]
                    sfi_parsed[component.name] = ext_len

                # Test if the component is the Extension Data (extension_data).
                elif component.name == 'extension_data':
                    # Get the extension length from the parsed data
                    ext_len = sfi_parsed.get('extension_len', 0)
                    # Read the extension data if it exists
                    if ext_len > 0:
                        # Parse the extension data
                        data = f.read(ext_len - 1)
                        sfi_parsed[component.name] = data.hex().upper()

        # Calculate the length of the SF data
        sfi_parsed["sf_data_len"] = sfi_parsed["sf_len"] - 8 - sfi_parsed.get("extension_len", 0)

        return sfi_parsed

    @staticmethod
    def _parse_sf(f, sfi_data: dict) -> bytes:
        """Parse les données du Structured Field."""
        # Calculer la longueur des données SF
        # sf_len inclut : sf_len (2) + sf_id (3) + flags (1) + reserved (2) + extension (si présente) + data
        # Donc data_len = sf_len - 8 - extension_len
        sf_len = sfi_data['sf_len']
        data_len = sf_len - 8  # Soustraire l'en-tête de base (8 bytes)

        # Soustraire la longueur de l'extension si présente
        if sfi_data.get('has_extension', False):
            ext_len = sfi_data.get('extension_len', 0)
            data_len -= ext_len

        # Lire les données du SF
        sf_data = f.read(data_len)
        return sf_data

