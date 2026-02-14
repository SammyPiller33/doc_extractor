
# AFP Document Inspector

## Overview

**AFP Document Inspector** is a multi-format document analysis and parsing tool designed for research and experimentation. It enables inspection of the internal structure of various production chain file formats through an extensible architecture based on format-specific parsing strategies.

The tool leverages an application routing component that automatically resolves and invokes the appropriate parsing strategy based on the provided file type. This architecture adheres to SOLID principles (Single Responsibility, Open/Closed, Dependency Inversion), cleanly separating routing logic from format-specific business logic.

## Features

- **Extensible Architecture**: Easily add new format parsers through the dispatcher pattern
- **Stream Processing**: Efficient memory usage for large files
- **Configurable Filtering**: Optional JSON-based configuration for selective parsing
- **Multiple Output Formats**: Currently supports JSON output with extensible writer system
- **Production-Ready Logging**: Comprehensive logging with performance metrics

## Usage

### Command Line Interface

The tool requires the following arguments:
`bash python main.py -f <file_path> -t <file_type> [-c <config_path>] [-o <output_format>]`

**Arguments:**
- `-f, --file` (required): Path to the file to analyze (must be valid and accessible)
- `-t, --type` (required): File format type
  - Currently supported: `afp`
  - Planned: PDF, PostScript, PCL, etc.
- `-c, --config` (optional): Path to JSON configuration file for filtering
- `-o, --output-format` (optional): Output format (default: `json`)

### Output

The tool generates a structured JSON file containing the parsed document hierarchy. For AFP files, the output includes:
- Document structure (documents, pages)
- Metadata (Tag Logical Elements)
- Media information (paper trays)
- Annotations (No Operation fields)

Output file naming convention: `<input_file>_structure.<format>`

## Architecture

### Core Components

├── dispatcher.py # Routes processing to format-specific parsers 
├── main.py # Application entry point and workflow orchestration 
├── cli/ # Command-line interface 
├── parser/ # Format-specific parsers (AFP, etc.) 
├── processor/ # Stream processing logic 
├── writer/ # Output format writers 
├── domain/ # Business domain models 
└── logger/ # Logging configuration

### Design Patterns

- **Strategy Pattern**: Format-specific parsers implement common interfaces
- **Factory Pattern**: Writers and processors are created via factories
- **Dependency Injection**: Components receive dependencies at initialization
- **Context Manager**: Resources (files, streams) are properly managed

## AFP Format Reference

### Overview

AFP (Advanced Function Presentation) is an IBM-developed data format for document presentation and printing. It's widely used in high-volume production environments for transactional documents (invoices, bank statements, etc.).

### Key Concepts

#### MO:DCA (Mixed Object Document Content Architecture)

**Definition**: A standardized format for document presentation in the AFP environment. MO:DCA enables:
- Document storage and retrieval in archives
- Viewing, annotation, and printing
- Presentation fidelity through resource objects
- Integration of different data object types into a single data stream

**Data Stream**: A continuous ordered stream of data elements and objects conforming to a given format.

#### Structured Fields

Structured Fields are the fundamental building blocks of AFP documents. They encode MO:DCA commands and consist of:

1. **Structured Field Introducer (SFI)**: Identifies the command, specifies total length, and provides control information
2. **Data**: Defines the effect of the structured field through parameters

##### Structured Field Introducer Format

| Offset | Name      | Description                                                      |
|--------|-----------|------------------------------------------------------------------|
| 0-1    | SFLength  | Total length of the structured field, including the introducer  |
| 2-4    | SFTypeID  | Unique identifier for the structured field type                 |
| 5      | Flags     | Control flags (e.g., extension presence indicator)              |
| 6-7    | Reserved  | Reserved bytes                                                   |
| 8-9    | Extension | Optional extension (present if bit 0 of Flags is B'1')          |

**Notes**:
- Bytes use big-endian byte order (byte 0 is most significant)
- Bits use big-endian bit order (bit 0 is most significant)
- Extensions can add up to 255 bytes to the introducer
- Some platforms wrap structured fields with additional bytes (e.g., X'5A' prefix)

##### Structured Field Data

The data section follows the introducer and contains zero or more parameters with format-specific information.

**Processing Order**: Structured fields are processed sequentially in the order they appear in the data stream, unless otherwise specified.

#### Object Content Architectures (OCAs)

AFP supports multiple data types, each with unique processing requirements defined by its OCA:

**Data Objects** (presentation content):
- **PTOCA** (Presentation Text Object Content Architecture): Text content
- **IOCA** (Image Object Content Architecture): Raster images
- **GOCA** (Graphics Object Content Architecture): Vector graphics
- **BCOCA** (Barcode Object Content Architecture): Barcodes

**Resource Objects** (reusable components):
- **FOCA** (Font Object Content Architecture): Fonts
- **CMOCA** (Color Map Object Content Architecture): Color definitions
- **MOCA** (Metadata Object Content Architecture): Metadata

**Object Containers**: Non-OCA objects (TIFF, EPS, PDF) can be carried in MO:DCA envelopes or referenced externally.

**Envelope Architectures**: MO:DCA defines envelopes for common resources:
- Form Definitions: Managing page production on physical media
- Overlays: Electronic storage of form data
- Indexes: Page indexing and tagging

#### Document Hierarchy

AFP documents follow a hierarchical structure:

Print File (BPF/EPF) 
├── Resource Groups (BRG/ERG) 
└── Documents (BDT/EDT) 
    └── Pages (BPG/EPG) 
        ├── Text Objects 
        ├── Graphic Objects 
        ├── Image Objects 
        └── Other Objects

**Delimiters**:
- **BPF/EPF**: Begin/End Print File
- **BRG/ERG**: Begin/End Resource Group
- **BDT/EDT**: Begin/End Document
- **BPG/EPG**: Begin/End Page

#### Document Indexing

MO:DCA provides indexing functions based on document structure and application-defined tags.

**Index Elements**:
- **BDI/EDI**: Begin/End Document Index (delimiter)
- **IEL**: Index Element (references indexed objects)
- **TLE**: Tag Logical Element (content-based tagging)
- **LLE**: Link Logical Element (relationships)

**Indexed Objects**: Pages and page groups that can be referenced by the index.

### Official References

- [AFP Consortium - Official Documentation](https://www.afpconsortium.org/)
- [MO:DCA Reference (v10)](https://www.afpconsortium.org/uploads/1/1/8/4/118458708/modca-reference-10.pdf)
- [PTOCA Reference (v4)](https://www.afpconsortium.org/uploads/1/1/8/4/118458708/ptoca-reference-04.pdf)
- [IOCA Reference (v9)](https://www.afpconsortium.org/uploads/1/1/8/4/118458708/ioca-reference-09.pdf)

## Development

### Requirements

- Python 3.8+
- Dependencies listed in project requirements

### Extending the Tool

**Adding a New Format Parser**:
1. Implement the `Processor` interface in `processor/`
2. Register the parser in `dispatcher.py`'s `init_dispatcher()`
3. Add format-specific models in `domain/`

**Adding a New Output Format**:
1. Implement the `Writer` abstract class in `writer/`
2. Register the writer in `writer_factory.py`
3. Add the format to `OUTPUT_FORMATS` in `cli/cli.py`

## License

See LICENSE file for details.

## TODO

- [ ] Abstract writer implementations
- [ ] Enhanced configuration management
- [ ] Comprehensive error handling
- [ ] Unit and integration tests
- [ ] Support for additional formats (PDF, PostScript, PCL)

