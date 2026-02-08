"""
Builder for constructing AFP document structure from streamed structured fields.
Handles hierarchical relationships and maintains sophisticated counters.
"""
from typing import Dict, Any

from processor.afp.afp_document_structure import (
    AFPDocumentStructure, AFPNode, SFInfo, TripletInfo, SFType
)


class AFPStructureBuilder:
    """
    Builds a hierarchical JSON structure from streamed AFP structured fields.
    Maintains stacks for tracking Begin/End pairs and manages counters.
    """

    # Mapping of SF names to their types and Begin/End pairs
    SF_MAPPINGS = {
        'BDT': (SFType.DOCUMENT, 'begin'),
        'EDT': (SFType.DOCUMENT, 'end'),
        'BPG': (SFType.PAGE, 'begin'),
        'EPG': (SFType.PAGE, 'end'),
        'BNG': (SFType.GROUP, 'begin'),
        'ENG': (SFType.GROUP, 'end'),
    }

    def __init__(self, file_path: str, file_size: int):
        """Initialize the builder with file information."""
        self.structure = AFPDocumentStructure(
            file_path=file_path,
            file_size=file_size
        )

        # Stack for tracking open nodes at each level
        self.document_stack: list[AFPNode] = []
        self.page_stack: list[AFPNode] = []
        self.group_stack: list[AFPNode] = []

        # Global counters for each type
        self.global_counters = {
            SFType.DOCUMENT: 0,
            SFType.PAGE: 0,
            SFType.GROUP: 0
        }

        # Sequence counter for all SFs
        self.sf_sequence = 0

        # Current offset in file
        self.current_offset = 0

        # Statistics by SF name
        self.sf_statistics: Dict[str, int] = {}

    def add_structured_field(self, sf_data: Dict[str, Any]) -> None:
        """
        Add a structured field to the document structure.

        Args:
            sf_data: Dictionary containing sf_name, sfi_data, and sf_data
        """
        sf_name = sf_data['sf_name']
        sfi_data = sf_data['sfi_data']
        parsed_data = sf_data['sf_data']

        # Update statistics
        self.sf_statistics[sf_name] = self.sf_statistics.get(sf_name, 0) + 1
        self.structure.total_sf_count += 1

        # Create SF info
        sf_info = self._create_sf_info(sf_name, sfi_data, parsed_data)

        # Update offset for next SF
        self.current_offset += sfi_data['sf_len'] + 1  # +1 for carriage control

        # Check if this is a Begin/End SF
        if sf_name in self.SF_MAPPINGS:
            sf_type, begin_or_end = self.SF_MAPPINGS[sf_name]

            if begin_or_end == 'begin':
                self._handle_begin_sf(sf_type, sf_info)
            else:  # end
                self._handle_end_sf(sf_type, sf_info)
        else:
            # Other SFs: add to current context or orphans
            self._handle_other_sf(sf_info)

    def _create_sf_info(self, sf_name: str, sfi_data: Dict, parsed_data: Any) -> SFInfo:
        """Create an SFInfo object from parsed data."""
        sf_info = SFInfo(
            sf_name=sf_name,
            sf_id=sfi_data['sf_id'].hex().upper(),
            offset=self.current_offset,
            length=sfi_data['sf_len'],
            sequence=self.sf_sequence
        )
        self.sf_sequence += 1

        # Extract triplets if present
        if isinstance(parsed_data, dict):
            if 'triplets' in parsed_data:
                for triplet in parsed_data['triplets']:
                    triplet_info = self._extract_triplet_info(triplet)
                    sf_info.triplets.append(triplet_info)

            # Store other parsed data as raw
            if 'raw_data' in parsed_data:
                sf_info.raw_data = parsed_data['raw_data'].hex().upper()
        elif isinstance(parsed_data, bytes):
            sf_info.raw_data = parsed_data.hex().upper()

        return sf_info

    def _extract_triplet_info(self, triplet: Dict) -> TripletInfo:
        """Extract relevant information from a triplet."""
        t_id_hex = triplet['t_id'].hex().upper()
        t_len = triplet['t_len']

        # Try to get a meaningful name from triplet data
        name = "Unknown"
        data = {}

        # FQN triplet (0x02)
        if 'fqn_name' in triplet:
            name = "Fully Qualified Name"
            if isinstance(triplet['fqn_name'], bytes):
                data['fqn'] = triplet['fqn_name'].decode('utf-8', errors='replace')
            else:
                data['fqn'] = str(triplet['fqn_name'])

            if 'fqn_type' in triplet:
                data['fqn_type'] = triplet['fqn_type'].hex()
            if 'fqn_fmt' in triplet:
                data['fqn_fmt'] = triplet['fqn_fmt'].hex()

        # Attribute Value triplet (0x36)
        elif 'att_val' in triplet:
            name = "Attribute Value"
            if isinstance(triplet['att_val'], bytes):
                data['value'] = triplet['att_val'].decode('utf-8', errors='replace')
            else:
                data['value'] = str(triplet['att_val'])

        # Other triplets - store raw
        elif 'raw' in triplet:
            data['raw'] = triplet['raw'].hex().upper()

        return TripletInfo(t_id=t_id_hex, t_len=t_len, name=name, data=data)

    def _handle_begin_sf(self, sf_type: SFType, sf_info: SFInfo) -> None:
        """Handle a Begin structured field (BDT, BPG, BNG)."""
        # Create new node
        node = AFPNode(
            node_type=sf_type,
            begin_sf=sf_info,
            global_index=self.global_counters[sf_type]
        )

        # Determine parent and local index
        if sf_type == SFType.DOCUMENT:
            # Top level - add to structure
            node.local_index = len(self.structure.documents)
            self.structure.documents.append(node)
            self.document_stack.append(node)
            self.structure.document_count += 1

        elif sf_type == SFType.PAGE:
            # Add to current document
            if self.document_stack:
                parent = self.document_stack[-1]
                node.local_index = len(parent.children)
                parent.children.append(node)
            else:
                # Orphan page
                node.local_index = 0
                self.structure.orphan_sfs.append(sf_info)
                return
            self.page_stack.append(node)
            self.structure.page_count += 1

        elif sf_type == SFType.GROUP:
            # Add to current page or document
            if self.page_stack:
                parent = self.page_stack[-1]
            elif self.document_stack:
                parent = self.document_stack[-1]
            else:
                # Orphan group
                self.structure.orphan_sfs.append(sf_info)
                return

            node.local_index = len(parent.children)
            parent.children.append(node)
            self.group_stack.append(node)
            self.structure.group_count += 1

        # Increment global counter
        self.global_counters[sf_type] += 1

    def _handle_end_sf(self, sf_type: SFType, sf_info: SFInfo) -> None:
        """Handle an End structured field (EDT, EPG, ENG)."""
        # Pop from appropriate stack and set end SF
        if sf_type == SFType.DOCUMENT and self.document_stack:
            node = self.document_stack.pop()
            node.end_sf = sf_info
        elif sf_type == SFType.PAGE and self.page_stack:
            node = self.page_stack.pop()
            node.end_sf = sf_info
        elif sf_type == SFType.GROUP and self.group_stack:
            node = self.group_stack.pop()
            node.end_sf = sf_info
        else:
            # Orphan end field
            self.structure.orphan_sfs.append(sf_info)

    def _handle_other_sf(self, sf_info: SFInfo) -> None:
        """Handle other structured fields (NOP, IMM, TLE, etc.)."""
        # Add to the most specific current context
        if self.group_stack:
            parent = self.group_stack[-1]
        elif self.page_stack:
            parent = self.page_stack[-1]
        elif self.document_stack:
            parent = self.document_stack[-1]
        else:
            # No context - add to orphans
            self.structure.orphan_sfs.append(sf_info)
            return

        # Store in metadata for now (could be children if needed)
        if 'other_fields' not in parent.metadata:
            parent.metadata['other_fields'] = []
        parent.metadata['other_fields'].append(sf_info.to_dict())

    def finalize(self) -> AFPDocumentStructure:
        """
        Finalize the structure and return the completed document.
        Updates statistics and handles any unclosed nodes.
        """
        # Update statistics in structure
        self.structure.statistics = self.sf_statistics

        # Check for unclosed nodes
        if self.document_stack:
            for node in self.document_stack:
                if 'warnings' not in node.metadata:
                    node.metadata['warnings'] = []
                node.metadata['warnings'].append("Document not properly closed (missing EDT)")

        if self.page_stack:
            for node in self.page_stack:
                if 'warnings' not in node.metadata:
                    node.metadata['warnings'] = []
                node.metadata['warnings'].append("Page not properly closed (missing EPG)")

        if self.group_stack:
            for node in self.group_stack:
                if 'warnings' not in node.metadata:
                    node.metadata['warnings'] = []
                node.metadata['warnings'].append("Group not properly closed (missing ENG)")

        return self.structure