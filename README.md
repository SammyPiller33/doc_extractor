# doc inspector

## Description

**doc inspector** est un outil d'analyse et de parsing de documents multi-formats, conçu pour l'étude et l'expérimentation. Il permet d'inspecter la structure interne de différents types de fichiers issus de chaînes de production, en fournissant une architecture extensible basée sur des stratégies de parsing spécifiques à chaque format.

L'outil utilise un composant de routage applicatif qui, à partir du type de fichier fourni, résout et invoque automatiquement la stratégie de parsing appropriée. Cette architecture respecte les principes SOLID (SRP, OCP, DIP) en séparant clairement la logique de routage de la logique métier spécifique à chaque format.

## Usage

L'outil s'utilise en ligne de commande avec deux paramètres obligatoires :

- **Nom du fichier** : Chemin vers le fichier à analyser (doit être un fichier valide et accessible)
- **Type du fichier** : Format du document à parser
  - Formats supportés actuellement : `afp`
  - Formats à venir : PDF, PostScript, PCL, etc.

**Exemple :**
```bash
python inspect_doc.py chemin/vers/fichier.afp afp
```

## Références et spécifications des formats

Cette section rassemble la documentation technique nécessaire pour comprendre la structure interne des différents formats de fichiers supportés par l'outil. Elle s'appuie sur des sources officielles et des spécifications standardisées.

### AFP (Advanced Function Presentation)

#### Références

- [AFP Consortium - Documentation](https://www.afpconsortium.org/) - Ressources officielles
- [MODCA ref](https://www.afpconsortium.org/uploads/1/1/8/4/118458708/modca-reference-10.pdf)
- [PTOCA ref](https://www.afpconsortium.org/uploads/1/1/8/4/118458708/ptoca-reference-04.pdf)
- [IOCA ref](https://www.afpconsortium.org/uploads/1/1/8/4/118458708/ioca-reference-09.pdf)

#### Vue d'ensemble

##### MODCA

AFP est un format de données d'impression et de présentation de documents développé par IBM. Il est largement utilisé dans les environnements de production haute-volume (factures, relevés bancaires, documents transactionnels).
AFP and MO:DCA
A mixed object document is the collection of data objects that comprise the document's content, and the resources and formatting specifications that dictate the processing functions to be performed on the content.
The MO:DCAarchitecture is designed to integrate the different data object types into documents that can be interchanged as a single data stream.
data stream = a continuous ordered stream of data elements and objects conforming to a given format.
MO:DCA = MO:DCA is a standardized format for the presentation of documents in the AFP environment. The MO:DCA format supports storing and retrieving documents in an archive, viewing, annotation, and printing of documents or parts of
documents in local or distributed systems environments. Presentation fidelity is accommodated by including resource objects in the documents that reference them.
 It also provides syntactic and semantic rules governing their use to ensure that
different applications process them in a consistent manner.

##### Champs structurés

Les documents AFP sont structurés autour des **Structured Fields** :

the main MO:DCA structures and are used to encode MO:DCA commands. A structured field starts with an
introducer that uniquely identifies the command, provides a total length for the command, and specifies
additional control information such as whether padding bytes are present. The introducer is followed by up to
32,759 data bytes. Data may be encoded using fixed parameters, repeating groups, keywords, and triplets.


##### Objets

Plusieurs types de données dans un doc : texte, graphiques, images, codes barres.
object content architectures (OCAs)
 Each data object type has unique processing requirements. An Object Content
Architecture (OCA) has been established for each data object to define its respective syntax and semantics.
On peut avoir des data objects des des resource objets
- data objects : type unique de données comme un texte de présentation, vectoir graphics, raster mage et les controles pour présenter la donnée
- resource objects : collection d'instructions de présentation et des données. Référencés par leur nom et pouvant être stockés dans des librairies système.
Il y a des OCAs définis pour chaque type d'objet : 
- PTOCA : Page Text Object Content Architecture
- IOCA : Image Object Content Architecture
- AFP GOCA : Graphics Object Content Architecture
- BCOCA : Barcode Object Content Architecture
- FOCAS : Font Object Content Architecture
- CMOCA : Color Map Object Content Architecture
- MOCA : Metadata Object Content Architecture

object container
The MO:DCA architectures also support data objects that are not defined by object content architectures. Examples of such objects are Tag Image File Format (TIFF), Encapsulated PostScript® (EPS), and Portable Document Format (PDF). Such objects can be carried in a MO:DCA envelope called an object container, or they can be referenced without being enveloped in MO:DCA structures.

In addition to object content architectures, the MO:DCA architecture defines envelope architectures for objects of common value in the presentation environment. Examples of these are Form Definition resource objects for
managing the production of pages on the physical media, overlay resource objects that accommodate electronic storage of forms data, and index resource objects that support indexing and tagging of pages in a document.

##### Hiérarchie des objets

Au plus au niveau on a le print file délimité par les champs BPF et EPF
Il contient un groupe de resources BRG/ERG et des documents BDT/EDT
Chaque document BDT contient des pages BPG/EPG
Et les objets sont inclus dans les pages : image object, présentation text object, graphics objets, etc.

#### MODCA overview

##### Syntax des champs structurés

- Blocs binaires standardisés de longueur variable. Bytes are numbered from left to right beginning with byte zero, which is considered the high order (most significant) byte position. This is referred to as big-endian byte order.
-  Bits in a single byte are numbered from left to right beginning with bit zero, the most significant bit, and
continuing through bit seven, the least significant bit. This is referred to as big-endian bit order.
Structured fields are

Les Structured Fields MO:DCA se composent de deux parties : un **structured Field Introducer** (SFI) qui identifie la longueur et le type du structured field, et des **données** qui définissent l'effet du structured field. Les données sont contenues dans un ensemble de paramètres, qui peuvent eux-mêmes contenir d'autres structures de données et éléments de données. La longueur maximale d'un structured field est de 32 767 octets.

###### Structure Field Introducer

| Offset           | Name      | Description                          |
|------------------|-----------|--------------------------------------|
| 0-1              | SFLength  | Defines the length of the structured field, including itself.       |
| 2-4              | SFTypeID  | Length of structured field (2 bytes) |
| 5                | Flags     |                                      |
| 6-7              | Reserved  |                                      |
| 8-9 (optionnels) | Extension | seulement si bit 0 des Flags est B'1' |

Application Note: Some platforms include structured fields in a larger platform-specific record by surrounding the structured field with additional bytes (such as the X'5A' prefix).

Astructured field introducer may be extended by up to 255 bytes. The presence of an SFI extension is
indicated by a value of B'1' in bit 0 of the SFI flag byte. If an extension is present, the introducer is at least 8
bytes, but not more than 263 bytes, in length. The first byte of the extension specifies its length.

###### Structure Field Data

The structured field's data is contained in a parameter set that immediately follows the structured field's introducer.
Depending on the structured field and its purpose, the parameter set may contain zero or more parameters. If parameters are present, they contain specific information appropriate for the structured field.

###### Processing Order
Unless otherwise specified in a structured field's definition, all structured fields are processed in the order in
which they appear in the data stream. For example, if a presentation data stream contains a page with a text
object, an Include Page Overlay, a graphic object, a second Include Page Overlay, and an image object, in that
order, the objects are presented (imaged) on the page in that same order. That is, the text object is presented
first, the first overlay is presented second, the graphic object is presented third, the second overlay is
presented fourth, and the image object is presented last.

###### Structured Field Parameters
Astructured field is composed of a set of parameters that provides data and control information to processors
of the data stream. The MO:DCA architecture has established a length, a set of permissible values and a
functional definition for each structured field parameter.
Aparameter can be mandatory or optional.

#### Document indexing

The document index defined by the MO:DCA architecture provides functions for indexing the document based
on document structure and on application-defined document tags. The index is delimited by a Begin Document
Index structured field and an End Document Index structured field and may be located within the document or
external to the document. MO:DCA elements that may be indexed are pages and page groups. When
referenced by an index, they are called indexed objects. The MO:DCA elements within a document index that
reference indexed objects are Index Element (IEL) structured fields. The MO:DCA elements within a document
index that support content-based tagging are Tag Logical Element (TLE) structured fields.

Note that the IEL and TLE structured fields may
occur multiple times.
Begin Document Index (BDI)
Index Element (IEL)
Link Logical Element (LLE)
Tag Logical Element (TLE)
End Document Index (EDI)

