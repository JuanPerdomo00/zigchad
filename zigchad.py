#!/usr/bin/python3
# God Is First
# -*- coding: utf-8 -*-
# === Generate By Touchpy ===

# Copyright (C) <2024-05-07>  <jakepy>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import requests
import tarfile
import glob
import json
import os
import shutil

VERSION = "0.1.4"
ZIG_URL = "https://ziglang.org/download/index.json"
ZIG_RELEASES_FILE = "/tmp/.zigreleases.json"
BYTES_IN_KB = 1024
ZIG_VERSIONS_DIR = os.path.join(os.environ.get(
    "HOME", "/home/user"), ".zig_versions")


class Color:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"

    @staticmethod
    def green(text: str) -> str:
        return f"{Color.GREEN}{text}{Color.RESET}"

    @staticmethod
    def yellow(text: str) -> str:
        return f"{Color.YELLOW}{text}{Color.RESET}"

    @staticmethod
    def red(text: str) -> str:
        return f"{Color.RED}{text}{Color.RESET}"

    @staticmethod
    def cyan(text: str) -> str:
        return f"{Color.CYAN}{text}{Color.RESET}"


c = Color()


class RequestHandler:
    """Handles downloading and reading the JSON file from the official Zig website."""

    def __init__(self, url):
        self.url = url

    def download_json(self):
        """Downloads the JSON file from the Zig website to ZIG_RELEASES_FILE."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            with open(ZIG_RELEASES_FILE, "w") as f:
                f.write(response.text)
            return 0
        except requests.exceptions.RequestException as e:
            print(f"{c.red('Error:')} Failed to download JSON: {e}")
            return 1

    def read_json(self):
        """Reads and parses the JSON file, downloading it if necessary."""
        try:
            if not os.path.exists(ZIG_RELEASES_FILE):
                if self.download_json() != 0:
                    return None
            with open(ZIG_RELEASES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"{c.red('Error:')} Failed to read JSON: {e}")
            return None


class ZigReleaseInfo:
    """Manages Zig release information, listing versions and details."""

    def __init__(self, data):
        self.data = data

    def list_releases(self):
        """Displays available Zig versions and their release dates."""
        if not self.data:
            print(f"{c.red('Error:')} No data available.")
            exit(1)

        print(f"{c.cyan('Index'):>6} {
              c.green('Version'):>10} {c.yellow('Date'):>10}")
        print("-" * 30)
        for i, (version, info) in enumerate(self.data.items()):
            print(
                f"{c.cyan(f'[{i}]'):>6} {c.green(version):>10} {
                    c.yellow(info['date']):>10}"
            )
        exit(0)

    def info_version(self, version):
        """Displays detailed information for a specific Zig version."""
        if not self.data or version not in self.data:
            print(f"{c.red('Error:')} Version '{version}' not found.")
            print(
                f"{c.cyan(f'Use: {os.path.basename(__file__)
                                  } -h or --help for more info 🦎')}"
            )
            exit(1)

        print(f"{c.cyan(f'Details for version 🦎: {c.green(version)}')}\n")
        for key, value in self.data[version].items():
            if isinstance(value, dict):
                print(f"{c.green(key)}:")
                for sub_key, sub_value in value.items():
                    if sub_key == "size":
                        sub_value = self.human_size_utils(int(sub_value))
                    print(f"  {c.yellow(sub_key)}: {sub_value}")
            else:
                print(f"{c.green(key)}: {value}")
        exit(0)

    @staticmethod
    def human_size_utils(sbytes):
        """Converts bytes to a human-readable format."""
        units = ["B", "KB", "MB", "GB"]
        size = float(sbytes)
        unit_index = 0
        while size >= BYTES_IN_KB and unit_index < len(units) - 1:
            size /= BYTES_IN_KB
            unit_index += 1
        return f"{size:.2f} {units[unit_index]}"


class DownloadZigTar(ZigReleaseInfo):
    """Handles downloading and extracting Zig tar files."""

    def __init__(self, data, architecture, zig_version, zig_dir):
        super().__init__(data)
        self.architecture = architecture
        self.zig_version = zig_version
        self.file_tar = ""
        self.zig_dir = zig_dir

    def download(self, path):
        """Downloads and extracts a Zig tar file for the specified version and architecture."""
        if not self.data:
            print(f"{c.red('Error:')} No data available.")
            exit(1)

        url_tar = None
        for version, releases in self.data.items():
            if self.zig_version and version != self.zig_version:
                continue
            if self.architecture in releases:
                print(f"{c.yellow('Version:')} {version}")
                print(f"{c.yellow('Architecture:')} {self.architecture}")
                print(f"{c.cyan('Download Details:')}")
                print("-" * 30)
                for key, value in releases[self.architecture].items():
                    if key == "tarball":
                        url_tar = value
                    if key == "size":
                        value = self.human_size_utils(int(value))
                    print(f"{c.yellow(key)}: {value}")
                print()

        if url_tar is None:
            print(
                f"{c.red('Error:')} No download URL found for architecture '{
                    self.architecture}' and version '{self.zig_version}'."
            )
            print(
                f"{c.cyan(f'Use: {os.path.basename(__file__)
                                  } -h or --help for more info 🦎')}"
            )
            exit(1)

        response = requests.get(url_tar)
        if response.status_code == 200:
            self.file_tar = f"zig-{self.zig_version}.tar.xz"
            filename = (
                os.path.join(path, self.file_tar) if os.path.isdir(
                    path) else path
            )
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"{c.green('File downloaded successfully to:')} {filename}")

            self._extract_zig_version(filename, path)
            self._remove_tar(filename, path)
            exit(0)
        else:
            print(f"{c.red('Error:')} Failed to download file from URL: {url_tar}")
            exit(1)

    def _extract_zig_version(self, file, path):
        """Extracts the tar file to the specified path and renames the folder to zig-<version>."""
        try:
            with tarfile.open(file, "r:*") as tar:
                tar.extractall(path=path, filter="data")
            print(f"{c.green('Extracted to:')} {path}")

            # Rename extracted folder to zig-<version>
            extracted_folders = [
                f
                for f in os.listdir(path)
                if f.startswith("zig-") and os.path.isdir(os.path.join(path, f))
            ]
            for folder in extracted_folders:
                if folder != f"zig-{self.zig_version}":
                    src = os.path.join(path, folder)
                    dst = os.path.join(path, f"zig-{self.zig_version}")
                    if os.path.exists(dst):
                        print(
                            f"{c.red('Error:')} Folder {
                                dst} already exists, skipping rename."
                        )
                    else:
                        os.rename(src, dst)
                        print(f"{c.green('Renamed folder:')} {src} to {dst}")
        except tarfile.TarError as e:
            print(f"{c.red('Error:')} Failed to extract tar file: {e}")
            exit(1)

    def _remove_tar(self, file, path):
        """Removes the downloaded tar file."""
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"{c.green('Removed tar file:')} {file}")
            else:
                print(f"{c.red('Error:')} No tar file found at: {file}")
        except (PermissionError, FileNotFoundError) as e:
            print(f"{c.red('Error:')} Failed to remove tar file: {e}")


class InstalledZig:
    """Manages installed Zig versions."""

    def __init__(self, zig_dir):
        self.zig_folder = zig_dir

    def list_installed_versions(self):
        """Lists installed Zig versions."""
        if not os.path.exists(self.zig_folder):
            print(
                f"{c.red('Error:')} Zig versions directory does not exist: {
                    self.zig_folder}"
            )
            return

        versions = [
            f
            for f in os.listdir(self.zig_folder)
            if os.path.isdir(os.path.join(self.zig_folder, f)) and f.startswith("zig-")
        ]
        if not versions:
            print(f"{c.yellow('No Zig versions installed in:')} {
                  self.zig_folder}")
            return

        print(f"{c.cyan('Installed Zig Versions 🦎')}")
        print("-" * 30)
        for version in sorted(versions):
            print(f"{c.green(version)}")
        print()

    def rename_version(self, version, new_name):
        """Renames an installed Zig version folder."""
        src = os.path.join(self.zig_folder, f"zig-{version}")
        dst = os.path.join(self.zig_folder, new_name)
        if not os.path.exists(src):
            print(
                f"{c.red('Error:')
                   } Version 'zig-{version}' not found in {self.zig_folder}"
            )
            return
        if os.path.exists(dst):
            print(
                f"{c.red('Error:')} Destination name '{
                    new_name}' already exists in {self.zig_folder}"
            )
            return
        try:
            os.rename(src, dst)
            print(f"{c.green('Renamed:')} {src} to {dst}")
            # Update symlink if the renamed version was active
            symlink_path = os.path.join(self.zig_folder, "zig")
            if os.path.islink(symlink_path) and os.readlink(symlink_path).startswith(
                src
            ):
                os.remove(symlink_path)
                print(
                    f"{c.yellow('Removed active symlink:')} {
                        symlink_path} (version renamed)"
                )
        except (PermissionError, FileNotFoundError) as e:
            print(f"{c.red('Error:')} Failed to rename version: {e}")

    def use_version(self, version):
        """Creates a symbolic link to the zig binary of the specified version in zig_dir."""
        zig_binary = os.path.join(self.zig_folder, f"zig-{version}", "zig")
        symlink_path = os.path.join(self.zig_folder, "zig")
        if not os.path.exists(zig_binary):
            print(
                f"{c.red(
                    'Error:')} Zig binary not found for version 'zig-{version}' at {zig_binary}"
            )
            return
        try:
            if os.path.exists(symlink_path):
                os.remove(symlink_path)
                print(f"{c.green('Removed existing symlink:')} {symlink_path}")
            os.symlink(zig_binary, symlink_path)
            print(f"{c.green('Created symbolic link:')} {
                  symlink_path} -> {zig_binary}")
            # Check if zig_dir is in PATH
            path_dirs = os.environ.get("PATH", "").split(":")
            if self.zig_folder not in path_dirs:
                print(
                    f"{c.yellow('Warning:')} {
                        self.zig_folder} is not in your PATH. Add it to run 'zig' directly:"
                )
                print(f"{c.cyan(f'  export PATH=$PATH:{self.zig_folder}')}")
            else:
                print(f"{c.cyan('You can now use zig by running:')} zig")
        except (PermissionError, FileNotFoundError) as e:
            print(f"{c.red('Error:')} Failed to create symbolic link: {e}")

    def remove_version(self, version):
        """Removes a specific Zig version folder."""
        version_dir = os.path.join(self.zig_folder, f"zig-{version}")
        if not os.path.exists(version_dir):
            print(
                f"{c.red('Error:')
                   } Version 'zig-{version}' not found in {self.zig_folder}"
            )
            return
        try:
            shutil.rmtree(version_dir)
            print(f"{c.green('Removed version:')} {version_dir}")
            # Remove symlink if it points to the deleted version
            symlink_path = os.path.join(self.zig_folder, "zig")
            if os.path.islink(symlink_path) and os.readlink(symlink_path).startswith(
                version_dir
            ):
                os.remove(symlink_path)
                print(
                    f"{c.yellow('Removed active symlink:')} {
                        symlink_path} (version deleted)"
                )
        except (PermissionError, FileNotFoundError) as e:
            print(f"{c.red('Error:')} Failed to remove version: {e}")
        except Exception as e:
            print(f"{c.red('Unexpected error while removing version:')} {e}")


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Download and manage Zig versions 🦎", usage="zigchad [args]"
    )
    parser.add_argument(
        "--version",
        "-v",
        action="store_true",
        help="Prints the version and exits with status 0.",
    )
    parser.add_argument(
        "--list-releases",
        "-lr",
        action="store_true",
        help="Lists all available Zig versions.",
    )
    parser.add_argument(
        "--info-version-zig",
        "-ivz",
        metavar="ZIG_VERSION",
        help="Prints information for a specific Zig version.",
    )
    parser.add_argument(
        "--download",
        "-d",
        nargs=3,
        metavar=("VERSION", "ARCHITECTURE", "PATH"),
        help="Downloads a Zig binary for the specified version, architecture, and path.",
    )
    parser.add_argument(
        "--rename",
        "-r",
        nargs=2,
        metavar=("VERSION", "NEW_NAME"),
        help="Renames the extracted Zig folder for the specified version.",
    )
    parser.add_argument(
        "--use-version",
        "-uv",
        metavar="VERSION",
        help="Sets the specified Zig version as the active one by creating a symbolic link in zig_dir.",
    )
    parser.add_argument(
        "--remove-version",
        "-rv",
        metavar="VERSION",
        help="Removes the specified Zig version folder.",
    )
    parser.add_argument(
        "--list-versions-installed",
        "-lvi",
        action="store_true",
        help="Lists all installed Zig versions.",
    )
    parser.add_argument(
        "--zig-dir",
        default=ZIG_VERSIONS_DIR,
        metavar="DIR",
        help="Specifies the directory for Zig versions (default: ~/.zig_versions).",
    )
    return parser.parse_args()


def main():
    """Main function to handle command-line arguments and execute actions."""
    args = parse_args()
    request_handler = RequestHandler(ZIG_URL)
    data = request_handler.read_json()

    if not data and not args.version:
        print(
            f"{c.cyan(f'Use: {os.path.basename(__file__)
                              } -h or --help for more info 🦎')}"
        )
        exit(1)

    release_info = ZigReleaseInfo(data)
    installed_zig = InstalledZig(args.zig_dir)

    if args.list_releases:
        release_info.list_releases()
    elif args.info_version_zig:
        release_info.info_version(args.info_version_zig)
    elif args.download:
        version, architecture, path = args.download
        download = DownloadZigTar(data, architecture, version, args.zig_dir)
        download.download(path)
    elif args.version:
        print(f"{c.cyan(f'zigchad {VERSION}')
                 }\nWritten by Jakepys GH@JuanPerdomo00")
        exit(0)
    elif args.list_versions_installed:
        installed_zig.list_installed_versions()
    elif args.rename:
        version, new_name = args.rename
        installed_zig.rename_version(version, new_name)
    elif args.use_version:
        installed_zig.use_version(args.use_version)
    elif args.remove_version:
        installed_zig.remove_version(args.remove_version)
    else:
        print(
            f"{c.cyan(f'Use: {os.path.basename(__file__)
                              } -h or --help for more info 🦎')}"
        )
        exit(1)


if __name__ == "__main__":
    main()
