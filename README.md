# Decrypt PDFs

Batch-decrypt PDF files that share the same password by calling `qpdf`.

## What This Tool Does

- Prompts for a password
- Decrypts all `*.pdf` files in an input directory
- Writes decrypted files to an output directory with the same filenames

## Requirements

- Python 3.13+
- `qpdf` installed and available on `PATH`

Install `qpdf`:

- Ubuntu/Debian: `sudo apt install qpdf`
- macOS (Homebrew): `brew install qpdf`
- Windows (scoop): `scoop install qpdf`

## Setup

1. Clone this repository.
2. Move to the project directory.
3. Install toolchain:
   - (Recommended) Install mise: <https://mise.jdx.dev/getting-started.html>
   - Run `mise install`
   - Instead, you can install `uv` directly if you prefer: <https://docs.astral.sh/uv/getting-started/installation/>

## Usage

```bash
uv run main.py <input_dir> <output_dir>
```

Example:

```bash
uv run main.py ./encrypted_pdfs ./decrypted_pdfs
```

You will be prompted:

```text
Enter the PDF password:
```

## CLI Arguments

- `input_dir`: Directory containing encrypted PDF files
- `output_dir`: Directory to write decrypted PDF files (created automatically if missing)

## Behavior Notes

- Only files matching `*.pdf` in `input_dir` are processed.
- Processing is non-recursive (subdirectories are not scanned).
- Source files are never modified.
- If decryption fails for a file (wrong password, damaged PDF, etc.), the script prints an error and moves on.

## Troubleshooting

- `Error: 'qpdf' is not installed.`  
  Install `qpdf` and ensure it is available from your shell.
- No files processed  
  Confirm that `input_dir` contains files ending in `.pdf`.
- `Failed to decrypt: <filename>`  
  Verify the password and confirm the file is a valid encrypted PDF.

## Development

- Lint: `uv run ruff check .`

## License

Apache License 2.0. See `LICENSE`.
