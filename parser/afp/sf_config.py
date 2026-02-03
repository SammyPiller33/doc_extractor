"""
Module for defining structured field syntax, types, and related constants.
"""

import collections

CARRIAGE_CONTROL = 0x5A
"""Carriage control code for MODCA structured fields."""

#################################################
# ===== Structured field introducer syntax =====

SfiComponent = collections.namedtuple(typename='SfiFieldParam',
                                      field_names=['offset', 'length', 'name', 'mandatory'])
"""
Structured Field Introducer (SFI) component.

Attributes:
    offset (int): Starting position of the component in the field.
    length (int): Length of the component in bytes.
    name (str): Name of the component.
    mandatory (bool): Indicates whether the component is mandatory.
"""

SFI_SYNTAX = [
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

#################################################
# ===== Structured field introducer syntaxe =====

tripletConfig = collections.namedtuple(typename='tripletConfig',
                                       field_names=['sf_id', 'sf_type', 'syntax'])

SfConfig = collections.namedtuple(typename='SfConfig',
                                  field_names=['short_name', 'full_name', 'syntax'])

SF_TYPES = {  # Types of structured fields in MODCA reference
    # ID: SfConfig(short_name, full_name, syntax)
    0xD3A8C9: SfConfig("BAG", "Begin Active Environment Group", "syntax"),
    0xD3A8EB: SfConfig("BBC", "Begin Bar Code Object", "syntax"),
    0xD3EEEB: SfConfig("BDA", "Bar Code Data", "syntax"),
    0xD3A6EB: SfConfig("BDD", "Bar Code Data Descriptor", "syntax"),
    0xD3A8C4: SfConfig("BDG", "Begin Document Environment Group", "syntax"),
    0xD3A8A7: SfConfig("BDI", "Begin Document Index", "syntax"),
    0xD3A8A8: SfConfig("BDT", "Begin Document", "syntax"),
    0xD3A8CD: SfConfig("BFM", "Begin Form Map", "syntax"),
    0xD3A8BB: SfConfig("BGR", "Begin Graphics Object", "syntax"),
    0xD3A8FB: SfConfig("BIM", "Begin Image Object", "syntax"),
    0xD3A8CC: SfConfig("BMM", "Begin Medium Map", "syntax"),
    0xD3A8DF: SfConfig("BMO", "Begin Overlay", "syntax"),
    0xD3A8AD: SfConfig("BNG", "Begin Named Page Group", "syntax"),
    0xD3A892: SfConfig("BOC", "Begin Object Container", "syntax"),
    0xD3A8C7: SfConfig("BOG", "Begin Object Environment Group", "syntax"),
    0xD3A8A5: SfConfig("BPF", "Begin Print File", "syntax"),
    0xD3A8AF: SfConfig("BPG", "Begin Page", "syntax"),
    0xD3A85F: SfConfig("BPS", "Begin Page Segment", "syntax"),
    0xD3A89B: SfConfig("BPT", "Begin Presentation Text Object", "syntax"),
    0xD3A8C6: SfConfig("BRG", "Begin Resource Group", "syntax"),
    0xD3A8CE: SfConfig("BRS", "Begin Resource", "syntax"),
    0xD3A8D9: SfConfig("BSG", "Begin Resource Environment Group", "syntax"),
    0xD3A692: SfConfig("CDD", "Container Data Descriptor", "syntax"),
    0xD3A9C9: SfConfig("EAG", "End Active Environment Group", "syntax"),
    0xD3A9EB: SfConfig("EBC", "End Bar Code Object", "syntax"),
    0xD3A9C4: SfConfig("EDG", "End Document Environment Group", "syntax"),
    0xD3A9A7: SfConfig("EDI", "End Document Index", "syntax"),
    0xD3A9A8: SfConfig("EDT", "End Document", "syntax"),
    0xD3A9CD: SfConfig("EFM", "End Form Map", "syntax"),
    0xD3A9BB: SfConfig("EGR", "End Graphics Object", "syntax"),
    0xD3A9FB: SfConfig("EIM", "End Image Object", "syntax"),
    0xD3A9CC: SfConfig("EMM", "End Medium Map", "syntax"),
    0xD3A9DF: SfConfig("EMO", "End Overlay", "syntax"),
    0xD3A9AD: SfConfig("ENG", "End Named Page Group", "syntax"),
    0xD3A992: SfConfig("EOC", "End Object Container", "syntax"),
    0xD3A9C7: SfConfig("EOG", "End Object Environment Group", "syntax"),
    0xD3A9A5: SfConfig("EPF", "End Print File", "syntax"),
    0xD3A9AF: SfConfig("EPG", "End Page", "syntax"),
    0xD3A95F: SfConfig("EPS", "End Page Segment", "syntax"),
    0xD3A99B: SfConfig("EPT", "End Presentation Text Object", "syntax"),
    0xD3A9C6: SfConfig("ERG", "End Resource Group", "syntax"),
    0xD3A9CE: SfConfig("ERS", "End Resource", "syntax"),
    0xD3A9D9: SfConfig("ESG", "End Resource Environment Group", "syntax"),
    0xD3EEBB: SfConfig("GAD", "Graphics Data", "syntax"),
    0xD3A6BB: SfConfig("GDD", "Graphics Data Descriptor", "syntax"),
    0xD3A6FB: SfConfig("IDD", "Image Data Descriptor", "syntax"),
    0xD3B2A7: SfConfig("IEL", "Index Element", "syntax"),
    0xD3ABCC: SfConfig("IMM", "Invoke Medium Map", "syntax"),
    0xD3AFC3: SfConfig("IOB", "Include Object", "syntax"),
    0xD3EEFB: SfConfig("IPD", "Image Picture Data", "syntax"),
    0xD3AFAF: SfConfig("IPG", "Include Page", "syntax"),
    0xD3AFD8: SfConfig("IPO", "Include Page Overlay", "syntax"),
    0xD3AF5F: SfConfig("IPS", "Include Page Segment", "syntax"),
    0xD3B490: SfConfig("LLE", "Link Logical Element", "syntax"),
    0xD3ABEB: SfConfig("MBC", "Map Bar Code Object", "syntax"),
    0xD3A288: SfConfig("MCC", "Medium Copy Count", "syntax"),
    0xD3AB92: SfConfig("MCD", "Map Container Data", "syntax"),
    0xD3AB8A: SfConfig("MCF", "Map Coded Font", "syntax"),
    0xD3A688: SfConfig("MDD", "Medium Descriptor", "syntax"),
    0xD3ABC3: SfConfig("MDR", "Map Data Resource", "syntax"),
    0xD3A088: SfConfig("MFC", "Medium Finishing Control", "syntax"),
    0xD3ABBB: SfConfig("MGO", "Map Graphics Object", "syntax"),
    0xD3ABFB: SfConfig("MIO", "Map Image Object", "syntax"),
    0xD3A788: SfConfig("MMC", "Medium Modification Control", "syntax"),
    0xD3ABCD: SfConfig("MMD", "Map Media Destination", "syntax"),
    0xD3B1DF: SfConfig("MMO", "Map Medium Overlay", "syntax"),
    0xD3AB88: SfConfig("MMT", "Map Media Type", "syntax"),
    0xD3ABAF: SfConfig("MPG", "Map Page", "syntax"),
    0xD3ABD8: SfConfig("MPO", "Map Page Overlay", "syntax"),
    0xD3B15F: SfConfig("MPS", "Map Page Segment", "syntax"),
    0xD3AB9B: SfConfig("MPT", "Map Presentation Text", "syntax"),
    0xD3ABEA: SfConfig("MSU", "Map Suppression", "syntax"),
    0xD3EEEE: SfConfig("NOP", "No Operation", "syntax"),
    0xD3A66B: SfConfig("OBD", "Object Area Descriptor", "syntax"),
    0xD3AC6B: SfConfig("OBP", "Object Area Position", "syntax"),
    0xD3EE92: SfConfig("OCD", "Object Container Data", "syntax"),
    0xD3A7A8: SfConfig("PEC", "Presentation Environment Control", "syntax"),
    0xD3B288: SfConfig("PFC", "Presentation Fidelity Control", "syntax"),
    0xD3A6AF: SfConfig("PGD", "Page Descriptor", "syntax"),
    0xD3B1AF: SfConfig("PGP", "Page Position", "syntax"),
    0xD3A7AF: SfConfig("PMC", "Page Modification Control", "syntax"),
    0xD3ADC3: SfConfig("PPO", "Preprocess Presentation Object", "syntax"),
    0xD3B19B: SfConfig("PTD", "Presentation Text Data Descriptor", "syntax"),
    0xD3EE9B: SfConfig("PTX", "Presentation Text Data", "syntax"),
    0xD3A090: SfConfig("TLE", "Tag Logical Element", "syntax")
}
