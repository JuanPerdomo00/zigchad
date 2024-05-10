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
import enum
import json
import os
from cansii import CAnsii as c

VERSION: str = "0.1.1"
ZIG_WEG: str = "https://ziglang.org/download/index.json"
ZIG_RELEASES_FILE: str = "/tmp/.zigreleses.json"
BYTES_IN_KB: int = 1024


class RequestHandler:
    def __init__(self, url: str) -> None:
        self.url = url

    def download_json(self):
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

    def info_version(self, version: str):
        data = self.data
        version_releases = [k for k, _ in data.items()]
        if version in version_releases:
            print(f"Details for version: {c.green(version):>10}\n")
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
        if sbytes < BYTES_IN_KB:
            return f"{sbytes} B"
        elif sbytes < BYTES_IN_KB**2:
            return f"{sbytes / BYTES_IN_KB:.2f} KB"
        elif sbytes < BYTES_IN_KB**3:
            return f"{sbytes / BYTES_IN_KB ** 2:.2f} MB"
        else:
            return f"{sbytes / BYTES_IN_KB ** 3:.2f} GB"


class DownloadZigTar(ZigReleaseInfo):
    def __init__(self, data: dict, zig_version: str = "", shasum: str = ""):
        super().__init__(data)
        self.zig_version = zig_version
        self.shasum = shasum

    def download(self):
        data = self.data
        for k, v in data.items():
            print(k)


def parse_args():
    parse = argparse.ArgumentParser(
        description="Download and update zig versions", usage="zigpy [args]"
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
        metavar=(f"{c.green("[version zig]")}", f"{c.green("[shasum]")}"),
        nargs=2,
        help="Download Zig binary by providing the version and part of the shasum",
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
        version, shasum = args.download
        download = DownloadZigTar(data, version, shasum)
        download.download()
    elif args.version:
        print(f"zigpy {VERSION}\nWritten by Jakepys GH@JuanPerdomo00")
        exit(0)


if __name__ == "__main__":
    main()
