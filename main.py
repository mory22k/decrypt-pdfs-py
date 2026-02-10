# Copyright 2026 Keisuke Morita

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
import subprocess
import argparse
import getpass
import os
import re
import shutil
import sys
import tempfile


FILE_MODE_PATTERN = re.compile(r"^0?[0-7]{3}$")


def check_qpdf() -> None:
    """
    Check if 'qpdf' is installed. If not, print an error message and exit.
    """
    if shutil.which("qpdf") is None:
        print("Error: 'qpdf' is not installed.")
        print("Please install qpdf using the following command:")
        print("\n  # Ubuntu/Debian\n  sudo apt install qpdf")
        print("\n  # macOS (Homebrew)\n  brew install qpdf")
        print("\n  # Windows (scoop)\n  scoop install qpdf")
        sys.exit(1)


def parse_file_mode(value: str) -> int:
    """
    Parse file mode from octal text.

    Args:
        value (str): File mode in octal text, e.g. 600 or 0600

    Returns:
        int: Parsed octal mode
    """
    if not FILE_MODE_PATTERN.fullmatch(value):
        raise argparse.ArgumentTypeError(
            "Invalid mode. Use octal format like 600, 0600, or 0644."
        )
    return int(value, 8)


def decrypt_pdfs(
    input_dir: Path,
    output_dir: Path,
    password: str,
    output_mode: int | None = None,
    verbose: bool = False,
) -> None:
    """
    Decrypt PDF files in the input directory and save them to the output directory.

    Args:
        input_dir (Path): Directory containing encrypted PDFs
        output_dir (Path): Directory to save decrypted PDFs
        password (str): Password to decrypt PDFs
        output_mode (int | None): Optional output file mode
        verbose (bool): Show detailed qpdf error output
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    password_file_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", delete=False
        ) as password_file:
            password_file_path = Path(password_file.name)
            os.chmod(password_file_path, 0o600)
            password_file.write(password)
            password_file.flush()

        for pdf_file in input_dir.glob("*.pdf"):
            output_path = output_dir / pdf_file.name

            command = [
                "qpdf",
                f"--password-file={password_file_path}",
                "--decrypt",
                str(pdf_file),
                str(output_path),
            ]

            try:
                subprocess.run(command, check=True, capture_output=True, text=True)

                if output_mode is not None:
                    try:
                        os.chmod(output_path, output_mode)
                    except OSError as exc:
                        print(
                            f"Warning: Could not set permissions on {output_path.name}: {exc}"
                        )

                print(f"Decrypted: {pdf_file.name}")
            except subprocess.CalledProcessError as exc:
                print(f"Failed to decrypt: {pdf_file.name}")
                if verbose and exc.stderr:
                    print(exc.stderr.strip())
    finally:
        if password_file_path is not None:
            try:
                password_file_path.unlink(missing_ok=True)
            except OSError as exc:
                print(
                    f"Warning: Could not delete temporary password file: {exc}",
                    file=sys.stderr,
                )


def main():
    check_qpdf()

    parser = argparse.ArgumentParser(description="Batch decrypt PDF files using qpdf.")
    parser.add_argument(
        "input_dir", type=Path, help="Path to the directory containing encrypted PDFs."
    )
    parser.add_argument(
        "output_dir", type=Path, help="Path to the directory to save decrypted PDFs."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--strict-permissions",
        action="store_true",
        help="Set output PDF permissions to 0600 (owner read/write only).",
    )
    group.add_argument(
        "--file-mode",
        type=parse_file_mode,
        metavar="MODE",
        help="Set output PDF permissions with octal mode (e.g. 0644, 0600).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed qpdf error output on failures.",
    )

    args = parser.parse_args()

    password = getpass.getpass("Enter the PDF password: ")
    if "\n" in password or "\r" in password:
        print("Error: Password must not contain newline characters.")
        sys.exit(1)

    output_mode: int | None = None
    if args.strict_permissions:
        output_mode = 0o600
    elif args.file_mode is not None:
        output_mode = args.file_mode

    decrypt_pdfs(
        args.input_dir,
        args.output_dir,
        password,
        output_mode=output_mode,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
