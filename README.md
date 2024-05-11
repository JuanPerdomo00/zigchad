# ZigChad 🦎

ZigChad is a command-line tool for downloading and updating Zig versions. It allows you to list available Zig versions, get information about a specific version, and download Zig binaries.

## Features

- **List Releases**: View all available Zig versions along with their release dates.
- **Version Information**: Get detailed information about a specific Zig version, including download links and file sizes.
- **Download Zig Binaries**: Download Zig binaries for a specific version and architecture.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/JuanPerdomo00/zigchad
    ```

2. Navigate to the project directory:

    ```bash
    cd ZigChad
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the `zigchad.py` script with the desired options:

```bash
python zigchad.py [options]

Options

    --version, -v: Print the tool version.
    --list-releases, -lr: List all available Zig versions.
    --info-version-zig [ZIG_VERSION], -ivz [ZIG_VERSION]: Get information about a specific Zig version.
    --download [ZIG_VERSION] [ARCHITECTURE] [PATH], -d [ZIG_VERSION] [ARCHITECTURE] [PATH]: Download Zig binary by providing the version, architecture, and path.
```
Example:

```bash

python zigchad.py --list-releases
```
```bash

python zigchad.py --info-version-zig 0.11.0
```

```bash

python zigchad.py --download 0.11.0 x86_64-linux /path/to/save
```

# Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
License