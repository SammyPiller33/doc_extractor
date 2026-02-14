from typing import NamedTuple

#############################
# ===== Triplets syntax =====

TRPLT_CMPNT_TYPE_HEXA = 1
TRPLT_CMPNT_TYPE_CODE = 2
TRPLT_CMPNT_TYPE_PARAM = 3
TRPLT_CMPNT_TYPE_GID = 4
TRPLT_CMPNT_TYPE_RESERVED = 6
TRPLT_CMPNT_TYPE_CHAR = 7
TRPLT_CMPNT_TYPE_UBIN = 8

class TripletComponent(NamedTuple):
    offset: int
    length: int
    name: str
    type: int
    mandatory: bool

TRIPLET_INTRODUCER: list[TripletComponent] = [
    TripletComponent(0, 1, 't_len', TRPLT_CMPNT_TYPE_UBIN, True),
    TripletComponent(1, 1, 't_id', TRPLT_CMPNT_TYPE_CODE, True)
]

TRIPLET_DEFAULT_STRUCTURE: list[TripletComponent] = [
    TripletComponent(2, 0, 'content', TRPLT_CMPNT_TYPE_HEXA, True)
]

GCSGID_CPGID_CCSID_STRUCTURE: list[TripletComponent] = [
    TripletComponent(2, 2, 'id_1', TRPLT_CMPNT_TYPE_CODE, True),
    TripletComponent(3, 1, 'id_2', TRPLT_CMPNT_TYPE_CODE, True)
]

FQN_STRUCTURE: list[TripletComponent] = [
    TripletComponent(2, 1, 'fqn_type', TRPLT_CMPNT_TYPE_PARAM, True),
    TripletComponent(3, 1, 'fqn_fmt', TRPLT_CMPNT_TYPE_PARAM, True),
    TripletComponent(4, 0, 'fqn_name', TRPLT_CMPNT_TYPE_GID, True)
]

ATTR_VAL_STRUCTURE: list[TripletComponent] = [
    TripletComponent(2, 2, 'reserved', TRPLT_CMPNT_TYPE_RESERVED, True),
    TripletComponent(4, 0, 'att_val', TRPLT_CMPNT_TYPE_CHAR, False)
]

class Triplet(NamedTuple):
    short_name: str
    full_name: str
    struct: list[TripletComponent]

# Triplet definitions indexed by their ID (byte value)
TRIPLET_CONFIG: dict[bytes, Triplet] = {
    b'\x01': Triplet("GCSGID_CPGID_CCSID", "Coded Graphic Character Set Global ID", GCSGID_CPGID_CCSID_STRUCTURE),
    b'\x02': Triplet("FQN", "Fully Qualified Name", FQN_STRUCTURE),
    b'\x04': Triplet("MO", "Mapping Option", TRIPLET_DEFAULT_STRUCTURE),
    b'\x10': Triplet("ObjClass", "Object Classification", TRIPLET_DEFAULT_STRUCTURE),
    b'\x18': Triplet("MIS", "MODCA Interchange Set", TRIPLET_DEFAULT_STRUCTURE),
    b'\x1F': Triplet("FDS", "Font Descriptor Specification", TRIPLET_DEFAULT_STRUCTURE),
    b'\x21': Triplet("OFSS", "Object Function Set Specification", TRIPLET_DEFAULT_STRUCTURE),
    b'\x22': Triplet("ExtRLID", "Extended Resource Local ID", TRIPLET_DEFAULT_STRUCTURE),
    b'\x24': Triplet("RLID", "Resource Local ID", TRIPLET_DEFAULT_STRUCTURE),
    b'\x25': Triplet("RSN", "Resource Section Number", TRIPLET_DEFAULT_STRUCTURE),
    b'\x26': Triplet("CharRot", "Character Rotation", TRIPLET_DEFAULT_STRUCTURE),
    b'\x2D': Triplet("ObjByteOff", "Object Byte Offset", TRIPLET_DEFAULT_STRUCTURE),
    b'\x36': Triplet("AttrVal", "Attribute Value", ATTR_VAL_STRUCTURE),
    b'\x43': Triplet("DescPos", "Descriptor Position", TRIPLET_DEFAULT_STRUCTURE),
    b'\x45': Triplet("MEC", "Media Eject Control", TRIPLET_DEFAULT_STRUCTURE),
    b'\x46': Triplet("POCP", "Page Overlay Conditional Processing", TRIPLET_DEFAULT_STRUCTURE),
    b'\x47': Triplet("RUA", "Resource Usage Attribute", TRIPLET_DEFAULT_STRUCTURE),
    b'\x4B': Triplet("MU", "Measurement Units", TRIPLET_DEFAULT_STRUCTURE),
    b'\x4C': Triplet("OAS", "Object Area Size", TRIPLET_DEFAULT_STRUCTURE),
    b'\x4D': Triplet("AD", "Area Definition", TRIPLET_DEFAULT_STRUCTURE),
    b'\x4E': Triplet("ColSpec", "Color Specification", TRIPLET_DEFAULT_STRUCTURE),
    b'\x50': Triplet("ESID", "Encoding Scheme ID", TRIPLET_DEFAULT_STRUCTURE),
    b'\x56': Triplet("MMPN", "Medium Map Page Number", TRIPLET_DEFAULT_STRUCTURE),
    b'\x57': Triplet("ObjByteExt", "Object Byte Extent", TRIPLET_DEFAULT_STRUCTURE),
    b'\x58': Triplet("ObjSFOff", "Object Structured Field Offset", TRIPLET_DEFAULT_STRUCTURE),
    b'\x59': Triplet("ObjSFExt", "Object Structured Field Extent", TRIPLET_DEFAULT_STRUCTURE),
    b'\x5A': Triplet("ObjOff", "Object Offset", TRIPLET_DEFAULT_STRUCTURE),
    b'\x5D': Triplet("FHSF", "Font Horizontal Scale Factor", TRIPLET_DEFAULT_STRUCTURE),
    b'\x5E': Triplet("ObjCnt", "Object Count", TRIPLET_DEFAULT_STRUCTURE),
    b'\x62': Triplet("ODT", "Object Date and Timestamp", TRIPLET_DEFAULT_STRUCTURE),
    b'\x65': Triplet("Cmt", "Comment", TRIPLET_DEFAULT_STRUCTURE),
    b'\x68': Triplet("MO", "Medium Orientation", TRIPLET_DEFAULT_STRUCTURE),
    b'\x6C': Triplet("ROI", "Resource Object Include", TRIPLET_DEFAULT_STRUCTURE),
    b'\x70': Triplet("PSRM", "Presentation Space Reset Mixing", TRIPLET_DEFAULT_STRUCTURE),
    b'\x71': Triplet("PSMR", "Presentation Space Mixing Rule", TRIPLET_DEFAULT_STRUCTURE),
    b'\x72': Triplet("UDT", "Universal Date and Timestamp", TRIPLET_DEFAULT_STRUCTURE),
    b'\x74': Triplet("TS", "Toner Saver", TRIPLET_DEFAULT_STRUCTURE),
    b'\x75': Triplet("ColFid", "Color Fidelity", TRIPLET_DEFAULT_STRUCTURE),
    b'\x78': Triplet("FontFid", "Font Fidelity", TRIPLET_DEFAULT_STRUCTURE),
    b'\x80': Triplet("AttrQual", "Attribute Qualifier", TRIPLET_DEFAULT_STRUCTURE),
    b'\x81': Triplet("PPI", "Page Position Information", TRIPLET_DEFAULT_STRUCTURE),
    b'\x82': Triplet("ParamVal", "Parameter Value", TRIPLET_DEFAULT_STRUCTURE),
    b'\x83': Triplet("PresCtrl", "Presentation Control", TRIPLET_DEFAULT_STRUCTURE),
    b'\x84': Triplet("FRMT", "Font Resolution and Metric Technology", TRIPLET_DEFAULT_STRUCTURE),
    b'\x85': Triplet("FinOp", "Finishing Operation", TRIPLET_DEFAULT_STRUCTURE),
    b'\x86': Triplet("TextFid", "Text Fidelity", TRIPLET_DEFAULT_STRUCTURE),
    b'\x87': Triplet("MediaFid", "Media Fidelity", TRIPLET_DEFAULT_STRUCTURE),
    b'\x88': Triplet("FinFid", "Finishing Fidelity", TRIPLET_DEFAULT_STRUCTURE),
    b'\x8B': Triplet("DOFD", "Data Object Font Descriptor", TRIPLET_DEFAULT_STRUCTURE),
    b'\x8C': Triplet("LocSel", "Locale Selector", TRIPLET_DEFAULT_STRUCTURE),
    b'\x8E': Triplet("UP3IFinOp", "UP3I Finishing Operation", TRIPLET_DEFAULT_STRUCTURE),
    b'\x91': Triplet("CMRD", "Color Management Resource Descriptor", TRIPLET_DEFAULT_STRUCTURE),
    b'\x95': Triplet("RendInt", "Rendering Intent", TRIPLET_DEFAULT_STRUCTURE),
    b'\x96': Triplet("CMRTagFid", "CMR Tag Fidelity", TRIPLET_DEFAULT_STRUCTURE),
    b'\x97': Triplet("DevApp", "Device Appearance", TRIPLET_DEFAULT_STRUCTURE),
    b'\x9A': Triplet("ImgRes", "Image Resolution", TRIPLET_DEFAULT_STRUCTURE),
    b'\x9C': Triplet("OCPSS", "Object Container Presentation Space Size", TRIPLET_DEFAULT_STRUCTURE),
}
