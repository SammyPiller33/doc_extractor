from typing import NamedTuple

####################################

SF_DATA_CMPNT_TYPE_HEXA = 1       # Raw bytes (hex)
SF_DATA_CMPNT_TYPE_CHAR = 2       # Character data
SF_DATA_CMPNT_TYPE_TRIPLETS = 3    # Triplet

class FieldDataComponent(NamedTuple):
    offset: int
    length: int
    name: str
    type: int
    mandatory: bool

FIELD_DATA_DEFAULT_STRUCTURE: list[FieldDataComponent] = [
    FieldDataComponent(0, 0, "NA", SF_DATA_CMPNT_TYPE_HEXA, True)
]

TLE_DATA_STRUCTURE: list[FieldDataComponent] = [
    FieldDataComponent(0, 0, "TRIPLETS", SF_DATA_CMPNT_TYPE_TRIPLETS, True),
]

IMM_DATA_STRUCTURE: list[FieldDataComponent] = [
    FieldDataComponent(0, 7, "MMPName", SF_DATA_CMPNT_TYPE_CHAR, True),  # Name of the medium map to be invoked
    FieldDataComponent(8, 0,  "NA", SF_DATA_CMPNT_TYPE_HEXA, False)
]

NOP_DATA_STRUCTURE: list[FieldDataComponent] = [
    FieldDataComponent(0, 0, "UndfData", SF_DATA_CMPNT_TYPE_CHAR, True)
]

####################################
# ===== Structure field syntax =====

class SfConfig(NamedTuple):
    short_name: str
    full_name: str
    struct: list[FieldDataComponent]

SF_CONFIGS: dict[bytes, SfConfig] = {  # Types of structured fields in MODCA reference
    # ID: SfConfig(short_name, full_name, syntax)
    b'\xD3\xA8\xC9': SfConfig("BAG", "Begin Active Environment Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xEB': SfConfig("BBC", "Begin Bar Code Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xEE\xEB': SfConfig("BDA", "Bar Code Data", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA6\xEB': SfConfig("BDD", "Bar Code Data Descriptor", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xC4': SfConfig("BDG", "Begin Document Environment Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xA7': SfConfig("BDI", "Begin Document Index", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xA8': SfConfig("BDT", "Begin Document", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xCD': SfConfig("BFM", "Begin Form Map", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xBB': SfConfig("BGR", "Begin Graphics Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xFB': SfConfig("BIM", "Begin Image Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xCC': SfConfig("BMM", "Begin Medium Map", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xDF': SfConfig("BMO", "Begin Overlay", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xAD': SfConfig("BNG", "Begin Named Page Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\x92': SfConfig("BOC", "Begin Object Container", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xC7': SfConfig("BOG", "Begin Object Environment Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xA5': SfConfig("BPF", "Begin Print File", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xAF': SfConfig("BPG", "Begin Page", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\x5F': SfConfig("BPS", "Begin Page Segment", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\x9B': SfConfig("BPT", "Begin Presentation Text Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xC6': SfConfig("BRG", "Begin Resource Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xCE': SfConfig("BRS", "Begin Resource", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA8\xD9': SfConfig("BSG", "Begin Resource Environment Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA6\x92': SfConfig("CDD", "Container Data Descriptor", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xC9': SfConfig("EAG", "End Active Environment Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xEB': SfConfig("EBC", "End Bar Code Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xC4': SfConfig("EDG", "End Document Environment Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xA7': SfConfig("EDI", "End Document Index", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xA8': SfConfig("EDT", "End Document", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xCD': SfConfig("EFM", "End Form Map", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xBB': SfConfig("EGR", "End Graphics Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xFB': SfConfig("EIM", "End Image Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xCC': SfConfig("EMM", "End Medium Map", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xDF': SfConfig("EMO", "End Overlay", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xAD': SfConfig("ENG", "End Named Page Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\x92': SfConfig("EOC", "End Object Container", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xC7': SfConfig("EOG", "End Object Environment Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xA5': SfConfig("EPF", "End Print File", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xAF': SfConfig("EPG", "End Page", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\x5F': SfConfig("EPS", "End Page Segment", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\x9B': SfConfig("EPT", "End Presentation Text Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xC6': SfConfig("ERG", "End Resource Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xCE': SfConfig("ERS", "End Resource", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA9\xD9': SfConfig("ESG", "End Resource Environment Group", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xEE\xBB': SfConfig("GAD", "Graphics Data", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA6\xBB': SfConfig("GDD", "Graphics Data Descriptor", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA6\xFB': SfConfig("IDD", "Image Data Descriptor", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xB2\xA7': SfConfig("IEL", "Index Element", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\xCC': SfConfig("IMM", "Invoke Medium Map", IMM_DATA_STRUCTURE),
    b'\xD3\xAF\xC3': SfConfig("IOB", "Include Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xEE\xFB': SfConfig("IPD", "Image Picture Data", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAF\xAF': SfConfig("IPG", "Include Page", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAF\xD8': SfConfig("IPO", "Include Page Overlay", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAF\x5F': SfConfig("IPS", "Include Page Segment", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xB4\x90': SfConfig("LLE", "Link Logical Element", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\xEB': SfConfig("MBC", "Map Bar Code Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA2\x88': SfConfig("MCC", "Medium Copy Count", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\x92': SfConfig("MCD", "Map Container Data", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\x8A': SfConfig("MCF", "Map Coded Font", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA6\x88': SfConfig("MDD", "Medium Descriptor", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\xC3': SfConfig("MDR", "Map Data Resource", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA0\x88': SfConfig("MFC", "Medium Finishing Control", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\xBB': SfConfig("MGO", "Map Graphics Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\xFB': SfConfig("MIO", "Map Image Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA7\x88': SfConfig("MMC", "Medium Modification Control", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\xCD': SfConfig("MMD", "Map Media Destination", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xB1\xDF': SfConfig("MMO", "Map Medium Overlay", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\x88': SfConfig("MMT", "Map Media Type", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\xAF': SfConfig("MPG", "Map Page", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\xD8': SfConfig("MPO", "Map Page Overlay", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xB1\x5F': SfConfig("MPS", "Map Page Segment", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\x9B': SfConfig("MPT", "Map Presentation Text", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAB\xEA': SfConfig("MSU", "Map Suppression", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xEE\xEE': SfConfig("NOP", "No Operation", NOP_DATA_STRUCTURE),
    b'\xD3\xA6\x6B': SfConfig("OBD", "Object Area Descriptor", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAC\x6B': SfConfig("OBP", "Object Area Position", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xEE\x92': SfConfig("OCD", "Object Container Data", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA7\xA8': SfConfig("PEC", "Presentation Environment Control", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xB2\x88': SfConfig("PFC", "Presentation Fidelity Control", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA6\xAF': SfConfig("PGD", "Page Descriptor", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xB1\xAF': SfConfig("PGP", "Page Position", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA7\xAF': SfConfig("PMC", "Page Modification Control", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xAD\xC3': SfConfig("PPO", "Preprocess Presentation Object", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xB1\x9B': SfConfig("PTD", "Presentation Text Data Descriptor", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xEE\x9B': SfConfig("PTX", "Presentation Text Data", FIELD_DATA_DEFAULT_STRUCTURE),
    b'\xD3\xA0\x90': SfConfig("TLE", "Tag Logical Element", TLE_DATA_STRUCTURE)
}
