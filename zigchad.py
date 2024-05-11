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
import json
import os
from cansii import CAnsii as c

VERSION: str = "0.1.2"
ZIG_WEG: str = "https://ziglang.org/download/index.json"
ZIG_RELEASES_FILE: str = "/tmp/.zigreleses.json"
BYTES_IN_KB: int = 1024


class RequestHandler:
    """This class is only responsible for downloading and reading the json file that comes from the official zig page"""
    def __init__(self, url: str) -> None:
        self.url = url

    def download_json(self) -> int:
        """
        The `download_json` method is responsible for fetching the json file from the official zig website 
        and downloading it to the temporary tmp path specified in the `ZIG_RELEASES_FILE` command.

        Returns:
            int
        """
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                with open(ZIG_RELEASES_FILE, "w") as f:
                    f.write(response.text)
                return 0
            else:
                print(
                    f"Error: Failed to download JSON, error code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to make request: {e}")
        return 1

    def read_json(self) -> dict:
        """read the json file and parse it area and it will return the dictionary with all its attributes

        Returns:
            dict
        """
        if not os.path.exists(ZIG_RELEASES_FILE):
            if self.download_json() == 0:
                pass
            else:
                pass
        else:
            with open(ZIG_RELEASES_FILE, "r") as f:
                return json.load(f)
        return None


class ZigReleaseInfo:
    """
    The `Zig ReleaseInfo` class is one of the most important, 
    as it is responsible for validating and listing certain zig versions among all versions or a specific one.
    """
    def __init__(self, data):
        self.data = data

    def list_releases(self) -> None:
        """Prints the available versions of zig and the release date and ends with a successful output 0"""
        data = self.data
        if data:
            print(f"{'Version':>15} {'Date':>7}\n")
            for i, (version, _) in enumerate(data.items()):
                print(
                    f"{c.green(f'[{i}]'):<10} \t{version:<10} {data[version]['date']:<10}"
                )
            exit(0)

    def info_version(self, version: str) -> dict:
        """

        Args:
            version (str): _description_

        Returns:
            dict: _description_
        """
        data = self.data
        version_releases = [k for k, _ in data.items()]
        if version in version_releases:
            print(f"Details for version🦎: {c.green(version):>10}\n")
            for k, v in data[version].items():
                if isinstance(v, dict):
                    print(f"{c.green(k)}:")
                    for sub_k, sub_v in v.items():
                        if sub_k == "size":
                            sub_v = self.human_size_utils(int(sub_v))
                        print(f"  {c.yellow(sub_k)}: {sub_v}")
                else:
                    print(f"{c.green(k)}: {v}")
        else:
            print(f"Version [{c.red(version)}] not found.")
            print(
                f"{c.cyan(f'Use: {os.path.basename(__file__)} -h or --help for more info')}"
            )

        return data

    @staticmethod
    def human_size_utils(sbytes: int) -> str:
        """
        The static method `human_size_utils` 
        is only responsible for calculating the number of bytes and returning me in a more human-readable quantity.

        Args:
            sbytes (int)

        Returns:
            str
        """
        if sbytes < BYTES_IN_KB:
            return f"{sbytes} B"
        elif sbytes < BYTES_IN_KB**2:
            return f"{sbytes / BYTES_IN_KB:.2f} KB"
        elif sbytes < BYTES_IN_KB**3:
            return f"{sbytes / BYTES_IN_KB ** 2:.2f} MB"
        else:
            return f"{sbytes / BYTES_IN_KB ** 3:.2f} GB"


class DownloadZigTar(ZigReleaseInfo):
    """This class is the logic to download the tar file that is specified"""
    def __init__(self, data: dict, architecture: str, zig_version: str):
        super().__init__(data)
        self.architecture = architecture
        self.zig_version = zig_version

    def download(self, path: str) -> None:
        """
        The download method does more than one thing, it will show and parse by architecture if it exists and will download the tar, 
        if it does not exist it will not.

        Args:
            path (str)
        """
        data = self.data
        url_tar: str = None
        for version, releases in data.items():
            if self.zig_version and version != self.zig_version:
                continue
            for karchzig, varchzig in releases.items():
                if karchzig == self.architecture:
                    print(f"{c.yellow('Version')}: {version}")
                    print(f"{c.yellow('Architecture')}: {self.architecture}")
                    for sub_key, sub_value in varchzig.items():
                        if sub_key == "tarball":
                            url_tar = sub_value
                        if sub_key == "size":
                            sub_value = self.human_size_utils(int(sub_value))
                        print(f"{c.yellow(sub_key)}: {sub_value}")

        if url_tar is None:
            print(
                c.red(
                    f"No download URL found for architecture '{self.architecture}' and version '{self.zig_version}'. "
                )
            )
            print(
                c.red(
                    f"Use: Use: {os.path.basename(__file__)} -h or --help for more info 🦎"
                )
            )
            exit(1)

        response = requests.get(url_tar)
        if response.status_code == 200:
            if os.path.isdir(path):
                filename = os.path.join(
                    path, f"zig-{self.zig_version}-{self.architecture}.tar.xz"
                )
            else:
                filename = path

            with open(filename, "wb") as f:
                f.write(response.content)
                print(c.green(f"File downloaded successfully to: {filename}"))
                exit(0)

        else:
            print(f"Failed to download file from URL: {url_tar}")
            exit(1)


def parse_args():
    parse = argparse.ArgumentParser(
        description="Download and update zig versions 🦎", usage="zigchad [args]"
    )
    parse.add_argument(
        "--version",
        "-v",
        help="prints the version and ends with a successful output 0",
        action="store_true",
    )
    parse.add_argument(
        "--list-releases",
        "-lr",
        help="brings all available versions of zig",
        action="store_true",
    )
    parse.add_argument(
        "--info-version-zig",
        "-ivz",
        help="prints the information of a specific version",
        metavar=f"{c.green('[zig version]')}",
    )

    parse.add_argument(
        "--download",
        "-d",
        metavar=(
            f"{c.green('[version zig]')}",
            f"{c.green('[architecture]')}",
            f"{c.green('[path]')}",
        ),
        nargs=3,
        help="Download Zig binary by providing the version, architecture and path",
    )

    return parse.parse_args()


def main() -> None:
    args = parse_args()
    request_handler = RequestHandler(ZIG_WEG)
    data: dict = request_handler.read_json()

    release_info = ZigReleaseInfo(data)

    if args.list_releases:
        release_info.list_releases()
    elif args.info_version_zig:
        release_info.info_version(args.info_version_zig)
    elif args.download:
        version, architecture, path = args.download
        download = DownloadZigTar(data, architecture=architecture, zig_version=version)
        download.download(path)
    elif args.version:
        print(f"zigpy {VERSION}\nWritten by Jakepys GH@JuanPerdomo00")
        exit(0)
    else:
        print(f"Use: {os.path.basename(__file__)} -h or --help for more info 🦎")
        exit(1)


if __name__ == "__main__":
    main()
