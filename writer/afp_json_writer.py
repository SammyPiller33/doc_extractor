import orjson
from domain.afp import Afp, Document, Page, Tle

from writer.writer import Writer


class AFPJsonWriter(Writer):
    """Efficient streaming JSON writer for AFP documents."""

    def __init__(self, afp_file_name, output_path: str, buffer_size: int = 100):
        super().__init__(output_path, buffer_size=buffer_size)
        self._buffer_size = buffer_size
        self._buffer = []
        self._file = None
        self._is_first = True

        self._afp_file_name = afp_file_name

        # State tracking
        self._afp = None
        self._curr_doc = None
        self._doc_count = 0
        self._curr_page = None
        self._page_count = 0
        self._curr_obj = None
        self._cur_media = "NA"

    def __enter__(self):
        self._file = open(self.output_path, 'wb')
        self._file.write(b'{\n  "documents": [\n')

        self._afp = Afp(name=self._afp_file_name)
        self._curr_obj = self._afp

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()

        self._file.write(b'\n  ],\n  "afp": ')
        self._afp.set_nb_of_docs(self._doc_count)
        self._afp.set_nb_of_pages(self._page_count)
        self._file.write(orjson.dumps(self._afp.model_dump()))

        self._file.write(b'\n}')
        self._file.close()

    def write(self, data: dict) -> None:
        """Process and write AFP structured field data."""
        sf_name = data.get('sf_name')

        if sf_name == 'BNG':
            self._handle_begin_document()
        elif sf_name == 'BPG':
            self._handle_begin_page()
        elif sf_name == 'TLE':
            self._handle_tag_logical_element(data)
        elif sf_name == 'NOP':
            self._handle_no_operation(data)
        elif sf_name == 'IMM':
            self._handle_invoke_medium_map(data)

    def _handle_begin_document(self):
        """Handle BNG (Begin Named Group) - start of document."""
        self._doc_count += 1

        if self._doc_count % self._buffer_size == 0:
            self.flush()

        self._curr_doc = Document(doc_number=f"{self._doc_count}")
        self._curr_obj = self._curr_doc
        self._buffer.append(self._curr_doc)

    def _handle_begin_page(self):
        """Handle BPG (Begin Page) - start of page."""
        self._page_count += 1
        self._curr_page = Page(
            page_number=f"{self._page_count}",
            bac_papier=self._cur_media
        )
        self._curr_doc.add_page(self._curr_page)
        self._curr_obj = self._curr_page

    def _handle_tag_logical_element(self, data: dict):
        """Handle TLE (Tag Logical Element) - metadata."""
        tle_data = data.get('sf_data', {}).get('TRIPLETS', [])

        tle_name = next(
            (item['FQN'].get('fqn_name', '')
             for item in tle_data if 'FQN' in item),
            None
        )

        tle_value = next(
            (item['AttrVal'].get('att_val', '')
             for item in tle_data if 'AttrVal' in item),
            ''
        )

        if tle_name:
            self._curr_obj.add_tle(Tle(name=tle_name, value=tle_value))

    def _handle_no_operation(self, data: dict):
        """Handle NOP (No Operation) - comment/annotation."""
        nop_value = data.get('sf_data', {}).get('UndfData')
        if nop_value:
            self._curr_obj.add_nop(nop_value)

    def _handle_invoke_medium_map(self, data: dict):
        """Handle IMM (Invoke Medium Map) - paper tray info."""
        self._cur_media = data.get('sf_data', {}).get('MMPName', 'NA')

    def flush(self) -> None:
        """Write buffered documents to file."""
        if not self._buffer:
            return

        serialized = [
            orjson.dumps(doc.model_dump())
            for doc in self._buffer
        ]

        prefix = b'    ' if self._is_first else b',\n    '
        content = prefix + b',\n    '.join(serialized)

        self._file.write(content)
        self._buffer.clear()
        self._is_first = False

