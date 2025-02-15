# Decrypt PDFs

This script decrypts a pile of PDFs encrypted with a same password using QPDF.

## How to use

1. Install QPDF
    - https://github.com/qpdf/qpdf
    - On macOS: `brew install qpdf`
2. Install mise.
    - https://mise.jdx.dev/getting-started.html
    - On macOS: `brew install mise`
3. Clone this repository.
4. Install the dependencies.
    - Move to the directory where you cloned the repository.
    - Run `mise install`
    - Run `uv sync --no-dev`
5. Run the script.
    - Run `python decrypt_pdfs.py <path_to_folder_containing_pdfs> <path_to_output_folder>`
    - Enter the password.

## License
