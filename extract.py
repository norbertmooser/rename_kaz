"""
Text Information Extractor

This module provides functionality to extract specific information from text files,
particularly dates and IBAN numbers, and format them into a structured string.

Functions:
    extract_information(file_path: str) -> str:
        Extracts IBAN, start date, and end date information from a text file.

Example usage:
    result = extract_information("path/to/your/file.txt")
    print(result)
"""

import re
from typing import Optional


def extract_information(file_path: str) -> str:
    """
    Extracts IBAN, start date, and end date information from a text file.

    This function reads a file line by line, searching for patterns that match
    dates (in the format DD.MM.YYYY) and IBAN numbers (in the format DE followed
    by 20 digits, possibly with spaces). It then formats the extracted dates to
    YYMMDD and constructs a string combining the IBAN and the dates. If any
    information is not found, underscores (_) are used as placeholders.

    Args:
        file_path (str): The path to the text file to be read.

    Returns:
        str: A string formatted as "{IBAN}_{start_date}_{end_date}", where
             IBAN is the extracted IBAN number, start_date is the formatted
             start date, and end_date is the formatted end date.
    """

    date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})")
    iban_pattern = re.compile(r"DE\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{2}")

    start_date: Optional[str] = None
    end_date: Optional[str] = None
    iban_number: Optional[str] = None

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Check for dates in the line
            dates = date_pattern.findall(line)
            if len(dates) == 2:
                # Convert dates to YYMMDD format
                start_date = dates[0][8:10] + dates[0][3:5] + dates[0][0:2]
                end_date = dates[1][8:10] + dates[1][3:5] + dates[1][0:2]

            # Check for IBAN in the line
            iban_match = iban_pattern.search(line)
            if iban_match:
                iban_number = iban_match.group().replace(" ", "")  # Remove spaces

            # Stop searching if all information is found
            if start_date and end_date and iban_number:
                break

    # Construct the final string
    start_date = start_date if start_date else "_"
    end_date = end_date if end_date else "_"
    iban_number = iban_number if iban_number else "_"

    return f"{iban_number}_{start_date}_{end_date}"
