"""
Module for defining structured field syntax, types, and related constants.
"""

from typing import NamedTuple

CARRIAGE_CONTROL: bytes = b'\x5a'
"""Carriage control code for MODCA structured fields."""

################################################
# ===== Structured field introducer syntax =====

class SfiComponent(NamedTuple):
    offset: int
    length: int
    name: str
    mandatory: bool

"""
Structured Field Introducer (SFI) component.

Attributes:
    offset (int): Starting position of the component in the field.
    length (int): Length of the component in bytes.
    name (str): Name of the component.
    mandatory (bool): Indicates whether the component is mandatory.
"""

SFI: list[SfiComponent] = [
    SfiComponent(0, 2, 'sf_len', True),
    SfiComponent(2, 3, 'sf_id', True),
    SfiComponent(5, 1, 'flags', True),
    SfiComponent(6, 2, 'reserved', True),
    SfiComponent(8, 1, 'extension_len', False),
    SfiComponent(9, 0, 'extension_data', False)
]
"""
Structured Field Introducer syntax according to MODCA specification.

List of components defining the structure of an SFI:
    - sf_len: Total length of the structured field (mandatory)
    - sf_id: Structured field type identifier (mandatory)
    - flags: Control flags (mandatory)
    - reserved: Reserved bytes (mandatory)
    - extension_len: Extension data length (optional)
    - extension_data: Extension data (optional)
"""

#############################
# ===== Triplets syntax =====

class Triplet(NamedTuple):
    sf_id: int
    sf_type: int
    syntax: str

###########################
# ===== Fields syntax =====

class FieldData(NamedTuple):
    triplets: list[Triplet]

BAG_SYNTAX: FieldData = FieldData([])
BBC_SYNTAX: FieldData = FieldData([])
BDA_SYNTAX: FieldData = FieldData([])
BDD_SYNTAX: FieldData = FieldData([])
BDG_SYNTAX: FieldData = FieldData([])
BDI_SYNTAX: FieldData = FieldData([])
BDT_SYNTAX: FieldData = FieldData([])
BFM_SYNTAX: FieldData = FieldData([])
BGR_SYNTAX: FieldData = FieldData([])
BIM_SYNTAX: FieldData = FieldData([])
BMM_SYNTAX: FieldData = FieldData([])
BMO_SYNTAX: FieldData = FieldData([])
BNG_SYNTAX: FieldData = FieldData([])
BOC_SYNTAX: FieldData = FieldData([])
BOG_SYNTAX: FieldData = FieldData([])
BPF_SYNTAX: FieldData = FieldData([])
BPG_SYNTAX: FieldData = FieldData([])
BPS_SYNTAX: FieldData = FieldData([])
BPT_SYNTAX: FieldData = FieldData([])
BRG_SYNTAX: FieldData = FieldData([])
BRS_SYNTAX: FieldData = FieldData([])
BSG_SYNTAX: FieldData = FieldData([])
CDD_SYNTAX: FieldData = FieldData([])
EAG_SYNTAX: FieldData = FieldData([])
EBC_SYNTAX: FieldData = FieldData([])
EDG_SYNTAX: FieldData = FieldData([])
EDI_SYNTAX: FieldData = FieldData([])
EDT_SYNTAX: FieldData = FieldData([])
EFM_SYNTAX: FieldData = FieldData([])
EGR_SYNTAX: FieldData = FieldData([])
EIM_SYNTAX: FieldData = FieldData([])
EMM_SYNTAX: FieldData = FieldData([])
EMO_SYNTAX: FieldData = FieldData([])
ENG_SYNTAX: FieldData = FieldData([])
EOC_SYNTAX: FieldData = FieldData([])
EOG_SYNTAX: FieldData = FieldData([])
EPF_SYNTAX: FieldData = FieldData([])
EPG_SYNTAX: FieldData = FieldData([])
EPS_SYNTAX: FieldData = FieldData([])
EPT_SYNTAX: FieldData = FieldData([])
ERG_SYNTAX: FieldData = FieldData([])
ERS_SYNTAX: FieldData = FieldData([])
ESG_SYNTAX: FieldData = FieldData([])
GAD_SYNTAX: FieldData = FieldData([])
GDD_SYNTAX: FieldData = FieldData([])
IDD_SYNTAX: FieldData = FieldData([])
IEL_SYNTAX: FieldData = FieldData([])
IMM_SYNTAX: FieldData = FieldData([])
IOB_SYNTAX: FieldData = FieldData([])
IPD_SYNTAX: FieldData = FieldData([])
IPG_SYNTAX: FieldData = FieldData([])
IPO_SYNTAX: FieldData = FieldData([])
IPS_SYNTAX: FieldData = FieldData([])
LLE_SYNTAX: FieldData = FieldData([])
MBC_SYNTAX: FieldData = FieldData([])
MCC_SYNTAX: FieldData = FieldData([])
MCD_SYNTAX: FieldData = FieldData([])
MCF_SYNTAX: FieldData = FieldData([])
MDD_SYNTAX: FieldData = FieldData([])
MDR_SYNTAX: FieldData = FieldData([])
MFC_SYNTAX: FieldData = FieldData([])
MGO_SYNTAX: FieldData = FieldData([])
MIO_SYNTAX: FieldData = FieldData([])
MMC_SYNTAX: FieldData = FieldData([])
MMD_SYNTAX: FieldData = FieldData([])
MMO_SYNTAX: FieldData = FieldData([])
MMT_SYNTAX: FieldData = FieldData([])
MPG_SYNTAX: FieldData = FieldData([])
MPO_SYNTAX: FieldData = FieldData([])
MPS_SYNTAX: FieldData = FieldData([])
MPT_SYNTAX: FieldData = FieldData([])
MSU_SYNTAX: FieldData = FieldData([])
NOP_SYNTAX: FieldData = FieldData([])
OBD_SYNTAX: FieldData = FieldData([])
OBP_SYNTAX: FieldData = FieldData([])
OCD_SYNTAX: FieldData = FieldData([])
PEC_SYNTAX: FieldData = FieldData([])
PFC_SYNTAX: FieldData = FieldData([])
PGD_SYNTAX: FieldData = FieldData([])
PGP_SYNTAX: FieldData = FieldData([])
PMC_SYNTAX: FieldData = FieldData([])
PPO_SYNTAX: FieldData = FieldData([])
PTD_SYNTAX: FieldData = FieldData([])
PTX_SYNTAX: FieldData = FieldData([])
TLE_SYNTAX: FieldData = FieldData([])

####################################
# ===== Structure field syntax =====

class SfConfig(NamedTuple):
    short_name: str
    full_name: str
    syntax: FieldData = FieldData(
        []
    )

SF_TYPES: dict[bytes, SfConfig] = {  # Types of structured fields in MODCA reference
    # ID: SfConfig(short_name, full_name, syntax)
    b'\xD3\xA8\xC9': SfConfig("BAG", "Begin Active Environment Group", BAG_SYNTAX),
    b'\xD3\xA8\xEB': SfConfig("BBC", "Begin Bar Code Object", BBC_SYNTAX),
    b'\xD3\xEE\xEB': SfConfig("BDA", "Bar Code Data", BDA_SYNTAX),
    b'\xD3\xA6\xEB': SfConfig("BDD", "Bar Code Data Descriptor", BDD_SYNTAX),
    b'\xD3\xA8\xC4': SfConfig("BDG", "Begin Document Environment Group", BDG_SYNTAX),
    b'\xD3\xA8\xA7': SfConfig("BDI", "Begin Document Index", BDI_SYNTAX),
    b'\xD3\xA8\xA8': SfConfig("BDT", "Begin Document", BDT_SYNTAX),
    b'\xD3\xA8\xCD': SfConfig("BFM", "Begin Form Map", BFM_SYNTAX),
    b'\xD3\xA8\xBB': SfConfig("BGR", "Begin Graphics Object", BGR_SYNTAX),
    b'\xD3\xA8\xFB': SfConfig("BIM", "Begin Image Object", BIM_SYNTAX),
    b'\xD3\xA8\xCC': SfConfig("BMM", "Begin Medium Map", BMM_SYNTAX),
    b'\xD3\xA8\xDF': SfConfig("BMO", "Begin Overlay", BMO_SYNTAX),
    b'\xD3\xA8\xAD': SfConfig("BNG", "Begin Named Page Group", BNG_SYNTAX),
    b'\xD3\xA8\x92': SfConfig("BOC", "Begin Object Container", BOC_SYNTAX),
    b'\xD3\xA8\xC7': SfConfig("BOG", "Begin Object Environment Group", BOG_SYNTAX),
    b'\xD3\xA8\xA5': SfConfig("BPF", "Begin Print File", BPF_SYNTAX),
    b'\xD3\xA8\xAF': SfConfig("BPG", "Begin Page", BPG_SYNTAX),
    b'\xD3\xA8\x5F': SfConfig("BPS", "Begin Page Segment", BPS_SYNTAX),
    b'\xD3\xA8\x9B': SfConfig("BPT", "Begin Presentation Text Object", BPT_SYNTAX),
    b'\xD3\xA8\xC6': SfConfig("BRG", "Begin Resource Group", BRG_SYNTAX),
    b'\xD3\xA8\xCE': SfConfig("BRS", "Begin Resource", BRS_SYNTAX),
    b'\xD3\xA8\xD9': SfConfig("BSG", "Begin Resource Environment Group", BSG_SYNTAX),
    b'\xD3\xA6\x92': SfConfig("CDD", "Container Data Descriptor", CDD_SYNTAX),
    b'\xD3\xA9\xC9': SfConfig("EAG", "End Active Environment Group", EAG_SYNTAX),
    b'\xD3\xA9\xEB': SfConfig("EBC", "End Bar Code Object", EBC_SYNTAX),
    b'\xD3\xA9\xC4': SfConfig("EDG", "End Document Environment Group", EDG_SYNTAX),
    b'\xD3\xA9\xA7': SfConfig("EDI", "End Document Index", EDI_SYNTAX),
    b'\xD3\xA9\xA8': SfConfig("EDT", "End Document", EDT_SYNTAX),
    b'\xD3\xA9\xCD': SfConfig("EFM", "End Form Map", EFM_SYNTAX),
    b'\xD3\xA9\xBB': SfConfig("EGR", "End Graphics Object", EGR_SYNTAX),
    b'\xD3\xA9\xFB': SfConfig("EIM", "End Image Object", EIM_SYNTAX),
    b'\xD3\xA9\xCC': SfConfig("EMM", "End Medium Map", EMM_SYNTAX),
    b'\xD3\xA9\xDF': SfConfig("EMO", "End Overlay", EMO_SYNTAX),
    b'\xD3\xA9\xAD': SfConfig("ENG", "End Named Page Group", ENG_SYNTAX),
    b'\xD3\xA9\x92': SfConfig("EOC", "End Object Container", EOC_SYNTAX),
    b'\xD3\xA9\xC7': SfConfig("EOG", "End Object Environment Group", EOG_SYNTAX),
    b'\xD3\xA9\xA5': SfConfig("EPF", "End Print File", EPF_SYNTAX),
    b'\xD3\xA9\xAF': SfConfig("EPG", "End Page", EPG_SYNTAX),
    b'\xD3\xA9\x5F': SfConfig("EPS", "End Page Segment", EPS_SYNTAX),
    b'\xD3\xA9\x9B': SfConfig("EPT", "End Presentation Text Object", EPT_SYNTAX),
    b'\xD3\xA9\xC6': SfConfig("ERG", "End Resource Group", ERG_SYNTAX),
    b'\xD3\xA9\xCE': SfConfig("ERS", "End Resource", ERS_SYNTAX),
    b'\xD3\xA9\xD9': SfConfig("ESG", "End Resource Environment Group", ESG_SYNTAX),
    b'\xD3\xEE\xBB': SfConfig("GAD", "Graphics Data", GAD_SYNTAX),
    b'\xD3\xA6\xBB': SfConfig("GDD", "Graphics Data Descriptor", GDD_SYNTAX),
    b'\xD3\xA6\xFB': SfConfig("IDD", "Image Data Descriptor", IDD_SYNTAX),
    b'\xD3\xB2\xA7': SfConfig("IEL", "Index Element", IEL_SYNTAX),
    b'\xD3\xAB\xCC': SfConfig("IMM", "Invoke Medium Map", IMM_SYNTAX),
    b'\xD3\xAF\xC3': SfConfig("IOB", "Include Object", IOB_SYNTAX),
    b'\xD3\xEE\xFB': SfConfig("IPD", "Image Picture Data", IPD_SYNTAX),
    b'\xD3\xAF\xAF': SfConfig("IPG", "Include Page", IPG_SYNTAX),
    b'\xD3\xAF\xD8': SfConfig("IPO", "Include Page Overlay", IPO_SYNTAX),
    b'\xD3\xAF\x5F': SfConfig("IPS", "Include Page Segment", IPS_SYNTAX),
    b'\xD3\xB4\x90': SfConfig("LLE", "Link Logical Element", LLE_SYNTAX),
    b'\xD3\xAB\xEB': SfConfig("MBC", "Map Bar Code Object", MBC_SYNTAX),
    b'\xD3\xA2\x88': SfConfig("MCC", "Medium Copy Count", MCC_SYNTAX),
    b'\xD3\xAB\x92': SfConfig("MCD", "Map Container Data", MCD_SYNTAX),
    b'\xD3\xAB\x8A': SfConfig("MCF", "Map Coded Font", MCF_SYNTAX),
    b'\xD3\xA6\x88': SfConfig("MDD", "Medium Descriptor", MDD_SYNTAX),
    b'\xD3\xAB\xC3': SfConfig("MDR", "Map Data Resource", MDR_SYNTAX),
    b'\xD3\xA0\x88': SfConfig("MFC", "Medium Finishing Control", MFC_SYNTAX),
    b'\xD3\xAB\xBB': SfConfig("MGO", "Map Graphics Object", MGO_SYNTAX),
    b'\xD3\xAB\xFB': SfConfig("MIO", "Map Image Object", MIO_SYNTAX),
    b'\xD3\xA7\x88': SfConfig("MMC", "Medium Modification Control", MMC_SYNTAX),
    b'\xD3\xAB\xCD': SfConfig("MMD", "Map Media Destination", MMD_SYNTAX),
    b'\xD3\xB1\xDF': SfConfig("MMO", "Map Medium Overlay", MMO_SYNTAX),
    b'\xD3\xAB\x88': SfConfig("MMT", "Map Media Type", MMT_SYNTAX),
    b'\xD3\xAB\xAF': SfConfig("MPG", "Map Page", MPG_SYNTAX),
    b'\xD3\xAB\xD8': SfConfig("MPO", "Map Page Overlay", MPO_SYNTAX),
    b'\xD3\xB1\x5F': SfConfig("MPS", "Map Page Segment", MPS_SYNTAX),
    b'\xD3\xAB\x9B': SfConfig("MPT", "Map Presentation Text", MPT_SYNTAX),
    b'\xD3\xAB\xEA': SfConfig("MSU", "Map Suppression", MSU_SYNTAX),
    b'\xD3\xEE\xEE': SfConfig("NOP", "No Operation", NOP_SYNTAX),
    b'\xD3\xA6\x6B': SfConfig("OBD", "Object Area Descriptor", OBD_SYNTAX),
    b'\xD3\xAC\x6B': SfConfig("OBP", "Object Area Position", OBP_SYNTAX),
    b'\xD3\xEE\x92': SfConfig("OCD", "Object Container Data", OCD_SYNTAX),
    b'\xD3\xA7\xA8': SfConfig("PEC", "Presentation Environment Control", PEC_SYNTAX),
    b'\xD3\xB2\x88': SfConfig("PFC", "Presentation Fidelity Control", PFC_SYNTAX),
    b'\xD3\xA6\xAF': SfConfig("PGD", "Page Descriptor", PGD_SYNTAX),
    b'\xD3\xB1\xAF': SfConfig("PGP", "Page Position", PGP_SYNTAX),
    b'\xD3\xA7\xAF': SfConfig("PMC", "Page Modification Control", PMC_SYNTAX),
    b'\xD3\xAD\xC3': SfConfig("PPO", "Preprocess Presentation Object", PPO_SYNTAX),
    b'\xD3\xB1\x9B': SfConfig("PTD", "Presentation Text Data Descriptor", PTD_SYNTAX),
    b'\xD3\xEE\x9B': SfConfig("PTX", "Presentation Text Data", PTX_SYNTAX),
    b'\xD3\xA0\x90': SfConfig("TLE", "Tag Logical Element", TLE_SYNTAX)
}
