# Postbank Accout Statement Title Modifier README

## Overview
This module specializes in processing PDF Postbank Account statements. It provides a suite of functions tailored to extract information from these statements and effectively manage file naming based on the extracted data. The primary functionalities include:

## PDF Processing:

### Extract Information: 
Identifies and extracts specific data such as dates (formatted from DD.MM.YYYY to YYMMDD) and IBAN numbers directly from the PDF statements. The extracted data is used to create a structured string which integrates these elements seamlessly.
### Rename Original File: 
After extracting relevant information, the original PDF file is renamed based on a new basename derived from the extracted information, ensuring easy tracking and organization.

## Prerequisites

Ensure that Python and the required libraries are installed:
- Python (3.6 or newer)

The module includes functions to verify the presence of critical utilities such as `pdftotext`, `pdftk`, `ps2ascii`, and `pdf2ps` on the system. 
These checks are essential for ensuring that the necessary tools are available for handling PDF files in more complex applications that require 
text extraction, PDF manipulation, or format conversion.

## Installation

No specific installation steps required apart from setting up Python. Ensure that your Python environment is properly configured.

## Usage

### Command Line

Run the script with a path to a text file as an argument to extract the IBAN, start date, and end date:

```bash
python rename_kaz.py path/to/your/file.txt
