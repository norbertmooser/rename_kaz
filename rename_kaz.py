import sys
import os
import glob
from typing import List, Dict
from prereqs import check_all_tools_installed
from conversions import alter_filename, cleanup


def browse_pdfs(directory: str) -> List[str]:
    """Browse and list all PDF files in the given directory."""
    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    return pdf_files

def main() -> None:
    status: Dict[str, bool] = check_all_tools_installed()
    for tool, is_installed in status.items():
        if not is_installed:
            print(f"{tool}: Not Installed")
            sys.exit(1)
        print(f"{tool}: Installed")
    print("All required tools are installed.")

    # Check for command line arguments
    if len(sys.argv) > 1:
        directory: str = sys.argv[1]
    else:
        directory: str = os.getcwd()

    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        sys.exit(1)

    pdf_files: List[str] = browse_pdfs(directory)
    if not pdf_files:
        print(f"Error: No PDF files found in the '{directory}' directory.")
        sys.exit(1)

    print(f"PDF files found in the '{directory}' directory:")
    for pdf in pdf_files:
        alter_filename(pdf)

    cleanup()

if __name__ == "__main__":
    main()
