"""Point d'entrée – extraction de documents non structurés en JSON."""

import json
import sys
from pathlib import Path

try:
    from .extractors import extract_document
except ImportError:
    from extractors import extract_document

INPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "input"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "output"


def process_one(file_path: Path, output_path: Path) -> None:
    """Traite un fichier : détection du type, extraction, écriture JSON."""
    print(f"\n--- Traitement : {file_path.name} ---")

    document = extract_document(file_path)
    print(f"  Type détecté : {document.document_type}")

    result = document.model_dump(mode="json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"  OK → {output_path}")


def main() -> None:
    """Traite tous les fichiers de data/input/ ou un chemin passé en argument."""
    # Extensions supportées
    SUPPORTED_EXTS = {".pdf", ".docx", ".txt", ".text", ".xlsx", ".xls", ".csv"}
    
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if target.is_dir():
            files = sorted([f for f in target.iterdir() if f.suffix.lower() in SUPPORTED_EXTS])
        elif target.is_file():
            files = [target]
        else:
            print(f"Erreur : '{target}' n'existe pas.")
            sys.exit(1)
    else:
        files = sorted([f for f in INPUT_DIR.iterdir() if f.suffix.lower() in SUPPORTED_EXTS])

    if not files:
        print("Aucun fichier supporté trouvé.")
        print(f"Extensions supportées : {', '.join(SUPPORTED_EXTS)}")
        sys.exit(0)

    print(f"=== NAF_ISB – {len(files)} fichier(s) à traiter ===")

    ok, ko = 0, 0
    for file in files:
        out = OUTPUT_DIR / (file.stem + ".json")
        try:
            process_one(file, out)
            ok += 1
        except Exception as exc:
            print(f"  ERREUR sur {file.name} : {exc}")
            ko += 1

    print(f"\n=== Résumé : {ok} réussi(s), {ko} erreur(s) ===")


if __name__ == "__main__":
    main()


