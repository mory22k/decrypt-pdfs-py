# Decrypt PDFs

Batch-decrypt PDF files that share the same password by calling `qpdf`.

## What This Tool Does

- Prompts for a password
- Decrypts all `*.pdf` files in an input directory
- Writes decrypted files to an output directory with the same filenames
- Supports optional strict output permissions for decrypted PDFs

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

With strict permissions:

```bash
uv run main.py ./encrypted_pdfs ./decrypted_pdfs --strict-permissions
```

With explicit output mode:

```bash
uv run main.py ./encrypted_pdfs ./decrypted_pdfs --file-mode 0600
```

You will be prompted:

```text
Enter the PDF password:
```

## CLI Arguments

- `input_dir`: Directory containing encrypted PDF files
- `output_dir`: Directory to write decrypted PDF files (created automatically if missing)
- `--strict-permissions`: Set decrypted PDF permissions to `0600`
- `--file-mode MODE`: Set decrypted PDF permissions with octal mode (for example `0644`, `0600`)
- `--verbose`: Show detailed `qpdf` error output for failed files

## Behavior Notes

- Only files matching `*.pdf` in `input_dir` are processed.
- Processing is non-recursive (subdirectories are not scanned).
- Source files are never modified.
- If decryption fails for a file (wrong password, damaged PDF, etc.), the script prints an error and moves on.
- Passwords are passed to `qpdf` through a temporary password file (`--password-file`), not through command-line password arguments.
- By default, decrypted output permissions follow normal OS file-creation behavior (`umask`).
- When `--strict-permissions` or `--file-mode` is specified, permissions are explicitly applied after successful decryption.

## Security Notes (Important)

- Decrypted PDFs are plaintext and may contain sensitive information. Handle them with strict care.
- If stricter access control is required, use `--strict-permissions` or `--file-mode 0600`.
- Delete decrypted PDFs as soon as they are no longer needed.
- This tool is not intended for use on shared multi-user computers.
- This tool is not intended for use in cloud environments.

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
