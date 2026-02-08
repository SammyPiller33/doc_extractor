from parser.file_parser import FileParser


class Processor:

    def __init__(self, file_parser: FileParser):
        self.parser: FileParser = file_parser

    def run(self):
        raise NotImplementedError

