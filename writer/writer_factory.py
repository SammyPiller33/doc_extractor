from writer.afp_json_writer import AFPJsonWriter
from writer.writer import Writer


def create_writer(output_format: str, file_name: str, output_path: str, **options) -> Writer:
    """
    Legacy factory function for creating writers.

    DEPRECATED: Use WriterFactory instead for better testability.

    Args:
        output_format: The desired output format (e.g., 'json', 'xml')
        output_path: Path where output should be written
        **options: Additional options for the writer

    Returns:
        Writer instance for the specified format

    Raises:
        ValueError: If the format is not supported
    """
    if output_format == 'json':
        return AFPJsonWriter(file_name, output_path, **options)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")