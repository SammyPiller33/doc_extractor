"""
Module for building a hierarchical JSON structure of AFP documents.
Tracks the logical structure with Begin/End pairs and sophisticated counters.
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class SFType(Enum):
    """Types of structured fields for tracking."""
    DOCUMENT = "DOCUMENT"  # BDT-EDT
    PAGE = "PAGE"  # BPG-EPG
    GROUP = "GROUP"  # BNG-ENG
    OTHER = "OTHER"


@dataclass
class TripletInfo:
    """Information extracted from a triplet."""
    t_id: str
    t_len: int
    name: str
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'id': self.t_id,
            'length': self.t_len,
            'name': self.name,
            'data': self.data
        }


@dataclass
class SFInfo:
    """Basic information about a structured field."""
    sf_name: str
    sf_id: str
    offset: int
    length: int
    sequence: int  # Global sequence number
    triplets: List[TripletInfo] = field(default_factory=list)
    raw_data: Optional[str] = None

    def to_dict(self) -> Dict:
        result = {
            'name': self.sf_name,
            'id': self.sf_id,
            'offset': self.offset,
            'length': self.length,
            'sequence': self.sequence
        }
        if self.triplets:
            result['triplets'] = [t.to_dict() for t in self.triplets]
        if self.raw_data:
            result['raw_data'] = self.raw_data
        return result


@dataclass
class AFPNode:
    """Represents a node in the AFP document tree."""
    node_type: SFType
    begin_sf: SFInfo
    end_sf: Optional[SFInfo] = None
    children: List['AFPNode'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Counters
    local_index: int = 0  # Index within parent (0-based)
    global_index: int = 0  # Global counter for this type (0-based)

    def is_complete(self) -> bool:
        """Check if the node has both begin and end SF."""
        return self.end_sf is not None

    def to_dict(self) -> Dict:
        result = {
            'type': self.node_type.value,
            'counters': {
                'local_index': self.local_index,
                'global_index': self.global_index
            },
            'begin': self.begin_sf.to_dict()
        }

        if self.end_sf:
            result['end'] = self.end_sf.to_dict()

        if self.metadata:
            result['metadata'] = self.metadata

        if self.children:
            result['children'] = [child.to_dict() for child in self.children]

        return result


@dataclass
class AFPDocumentStructure:
    """Root structure representing the entire AFP document."""
    file_path: str
    file_size: int
    documents: List[AFPNode] = field(default_factory=list)
    orphan_sfs: List[SFInfo] = field(default_factory=list)  # SFs not in a document

    # Global counters
    total_sf_count: int = 0
    document_count: int = 0
    page_count: int = 0
    group_count: int = 0

    # Detailed statistics
    statistics: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'file_info': {
                'path': self.file_path,
                'size': self.file_size
            },
            'counters': {
                'total_structured_fields': self.total_sf_count,
                'documents': self.document_count,
                'pages': self.page_count,
                'groups': self.group_count
            },
            'statistics': self.statistics,
            'documents': [doc.to_dict() for doc in self.documents],
            'orphan_fields': [sf.to_dict() for sf in self.orphan_sfs]
        }