"""
This module provides functionality to check the installation status of various PDF processing tools.

The module includes functions to verify the presence of critical utilities such as `pdftotext`, `pdftk`, `ps2ascii`, and `pdf2ps` on the system. 
These checks are essential for ensuring that the necessary tools are available for handling PDF files in more complex applications that require 
text extraction, PDF manipulation, or format conversion.

Functions:
    is_pdftotext_installed() -> bool:
        Checks if the `pdftotext` utility is installed on the system.
    is_pdftk_installed() -> bool:
        Checks if the `pdftk` utility is installed on the system.
    is_ps2ascii_installed() -> bool:
        Checks if the `ps2ascii` utility is installed on the system.
    is_pdf2ps_installed() -> bool:
        Checks if the `pdf2ps` utility is installed on the system.
    check_all_tools_installed() -> dict:
        Checks all required tools and returns a dictionary with the installation status of each.

The module can be executed as a script to perform a comprehensive check of all tools and print their installation status. This execution mode is useful for diagnostics and pre-deployment validation of an environment.

Example Usage:
    Running the module as a standalone script will check each tool and print the installation status:

    $ python this_module.py
    pdftotext: Installed
    pdftk: Not Installed
    ps2ascii: Installed
    pdf2ps: Installed
    All required tools are installed.
"""

import subprocess
import sys


def is_pdftotext_installed():
    """Check if pdftotext is installed."""
    try:
        subprocess.run(
            ["pdftotext", "-v"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_pdftk_installed():
    """Check if pdftk is installed."""
    try:
        subprocess.run(
            ["pdftk", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_ps2ascii_installed():
    """Check if ps2ascii is installed."""
    try:
        subprocess.run(
            ["ps2ascii", "-v"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_pdf2ps_installed():
    """Check if pdf2ps is installed."""
    try:
        result = subprocess.run(
            ["which", "pdf2ps"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.strip() != b""
    except subprocess.CalledProcessError:
        return False


def check_all_tools_installed():
    """Check if all required tools are installed and return their statuses."""
    tools_status = {
        "pdftotext": is_pdftotext_installed(),
        "pdftk": is_pdftk_installed(),
        "ps2ascii": is_ps2ascii_installed(),
        "pdf2ps": is_pdf2ps_installed(),
    }
    return tools_status


# Example usage
if __name__ == "__main__":
    status = check_all_tools_installed()
    for tool, is_installed in status.items():
        if not is_installed:
            print(f"{tool}: Not Installed")
            sys.exit(1)
        print(f"{tool}: Installed")
    print("All required tools are installed.")
