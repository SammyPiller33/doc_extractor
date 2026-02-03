import mimetypes
from pathlib import Path
from typing import Optional

def guess_mime_type(path: Path) -> Optional[str]:
    mime_type, _ = mimetypes.guess_type(str(path))
    return mime_type

if __name__ == "__main__":
    print(guess_mime_type(Path("../inspect_doc.py")))
    print(guess_mime_type(Path("../sample/01_Health_Coverage.pdf")))
    print(guess_mime_type(Path("../sample/01_Health_Coverage.html")))
    print(guess_mime_type(Path("../sample/01_Health_Coverage.afp"))) # afp pas dans la table MIME