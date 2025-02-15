# Copyright 2025 Keisuke Morita

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
import shutil
import sys


def check_qpdf() -> None:
    """
    Check if 'qpdf' is installed. If not, print an error message and exit.
    """
    if shutil.which("qpdf") is None:
        print("Error: 'qpdf' is not installed.")
        print("Please install qpdf using the following command:")
        print("\n  # macOS (Homebrew)\n  brew install qpdf")
        print("\n  # Ubuntu/Debian\n  sudo apt install qpdf")
        print("\n  # Windows (scoop)\n  scoop install qpdf")
        sys.exit(1)


def decrypt_pdfs(input_dir: Path, output_dir: Path, password: str) -> None:
    """
    Decrypt PDF files in the input directory and save them to the output directory.

    Args:
        input_dir (Path): Directory containing encrypted PDFs
        output_dir (Path): Directory to save decrypted PDFs
        password (str): Password to decrypt PDFs
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file in input_dir.glob("*.pdf"):
        output_path = output_dir / pdf_file.name

        command = [
            "qpdf",
            f"--password={password}",
            "--decrypt",
            str(pdf_file),
            str(output_path),
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Decrypted: {pdf_file.name}")
        except subprocess.CalledProcessError:
            print(f"Failed to decrypt: {pdf_file.name}")


def main():
    check_qpdf()

    parser = argparse.ArgumentParser(description="Batch decrypt PDF files using qpdf.")
    parser.add_argument(
        "input_dir", type=Path, help="Path to the directory containing encrypted PDFs."
    )
    parser.add_argument(
        "output_dir", type=Path, help="Path to the directory to save decrypted PDFs."
    )

    args = parser.parse_args()

    password = getpass.getpass("Enter the PDF password: ")

    decrypt_pdfs(args.input_dir, args.output_dir, password)


if __name__ == "__main__":
    main()
