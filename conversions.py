"""
This module provides functionality for processing PDF files, including extracting the first page,
converting to PS and text formats, extracting specific information (such as dates and IBAN),
and renaming files based on the extracted information.

Functions:
    extract_first_page(pdf_file: str) -> Optional[str]: Extract the first page of a PDF file using pdftk.
    convert_to_ps(pdf_file: str) -> Optional[str]: Convert the first page of a PDF to PS using pdf2ps.
    convert_ps_to_ascii(ps_file: str) -> Optional[str]: Convert a PS file to ASCII text using ps2ascii.
    convert_pdf_to_text_pdftotext(pdf_file: str) -> Optional[str]: Convert the first page of a PDF to ASCII text using pdftotext.
    extract_information(file_path: str) -> str: Extract information from a text file using regex patterns for date and IBAN.
    rename_pdf(pdf_file: str, new_basename: str) -> None: Rename the PDF file to 'new_basename.pdf'.
    alter_filename(pdf: str) -> None: Alter the filename of a PDF based on extracted information.
"""

import os
import re
import subprocess
from typing import Optional

TEMPFILENAME = "intermediate"
TEMPFILENAME_FIRST_PAGE = "temp_first_page"

def extract_first_page(pdf_file: str) -> Optional[str]:
    """Extract the first page of a PDF file using pdftk."""
    output_file = f"./kaz/{TEMPFILENAME}.pdf"
    try:
        subprocess.run(
            ["pdftk", pdf_file, "cat", "1", "output", output_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return output_file
    except subprocess.CalledProcessError as error:
        print(f"Error extracting first page from {pdf_file}: {error}")
        return None

def convert_to_ps(pdf_file: str) -> Optional[str]:
    """Convert the first page of a PDF to PS using pdf2ps."""
    first_page_pdf = extract_first_page(pdf_file)
    if not first_page_pdf:
        return None

    output_ps_file = f"./kaz/{TEMPFILENAME}.ps"
    try:
        command = ["pdf2ps", first_page_pdf, output_ps_file]
        subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        os.remove(first_page_pdf)
        return output_ps_file
    except subprocess.CalledProcessError as error:
        print(f"Error converting {first_page_pdf} to PS: {error}")
        return None

def convert_ps_to_ascii(ps_file: str) -> Optional[str]:
    """Convert a PS file to ASCII text using ps2ascii."""
    output_ascii_file = f"./kaz/{TEMPFILENAME}.ascii"
    try:
        command = ["ps2ascii", ps_file, output_ascii_file]
        subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return output_ascii_file
    except subprocess.CalledProcessError as error:
        print(f"Error converting {ps_file} to text: {error}")
        return None

def convert_pdf_to_text_pdftotext(pdf_file: str) -> Optional[str]:
    """Convert the first page of a PDF to ASCII text using pdftotext."""
    output_txt_file = f"./kaz/{TEMPFILENAME}.txt"
    try:
        command = ["pdftotext", "-f", "1", "-l", "1", pdf_file, output_txt_file]
        subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return output_txt_file
    except subprocess.CalledProcessError as error:
        print(f"Error converting {pdf_file} to text: {error}")
        return None

def extract_information(file_path: str) -> str:
    """Extract information from a text file using regex patterns for date and IBAN."""
    date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
    iban_pattern = re.compile(r"DE\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{2}")

    start_date, end_date, iban_number = None, None, None

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            dates = date_pattern.findall(line)
            if len(dates) == 2:
                start_date = dates[0][8:10] + dates[0][3:5] + dates[0][0:2]
                end_date = dates[1][8:10] + dates[1][3:5] + dates[1][0:2]

            iban_match = iban_pattern.search(line)
            if iban_match:
                iban_number = iban_match.group().replace(" ", "")

            if start_date and end_date and iban_number:
                break

    start_date = start_date if start_date else "_"
    end_date = end_date if end_date else "_"
    iban_number = iban_number if iban_number else "_"

    return f"{iban_number}_{start_date}_{end_date}"

def rename_pdf(pdf_file: str, new_basename: str) -> None:
    """Rename the PDF file to 'new_basename.pdf'."""
    pdf_dir = os.path.dirname(pdf_file)
    pdf_name = os.path.basename(pdf_file)
    pdf_ext = os.path.splitext(pdf_name)[1]
    new_name = os.path.join(pdf_dir, new_basename + pdf_ext)
    os.rename(pdf_file, new_name)
    print(f"Renamed {pdf_file} to {new_name}")

def alter_filename(pdf: str) -> None:
    """Alter the filename of a PDF based on extracted information."""
    print(pdf)
    if re.match(r"(?:.*/)?DE\d{20}_\d{6}_\d{6}\.pdf", pdf):
        return

    ps_file = convert_to_ps(pdf)
    if ps_file:
        ascii_file = convert_ps_to_ascii(ps_file)
        extracted_info = extract_information(ascii_file)
    else:
        extracted_info = "_____"

    if extracted_info == "_____":
        txt_file = convert_pdf_to_text_pdftotext(pdf)
        extracted_info = extract_information(txt_file)

    print(extracted_info)

    if extracted_info != "_____":
        rename_pdf(pdf, extracted_info)

def delete_file(file_path: str):
    """Delete a file."""
    try:
        os.remove(file_path)
    except OSError as error:
        print(f"Error deleting file {file_path}: {error}")

def cleanup() -> None:
    delete_file("./kaz/intermediate.ascii")
    delete_file("./kaz/intermediate.ps")
    delete_file("./kaz/intermediate.txt")