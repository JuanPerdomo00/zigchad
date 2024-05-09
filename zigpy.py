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
import re
from cansii import CAnsii as c


___version__ = "0.1"

class RequestPageZig:
    def __init__(self):
        self._path_file_json_zig = "/tmp/.zigreleses.json"
        self._url = "https://ziglang.org/download/index.json"

    def _human_size_utils(self, sbytes) -> str:
        """It is responsible for receiving the decimal number of bits and
        passing them to a conversion of Megabyte KiloBytes and Gigabytes

        Args:
            sbytes: is the argument that arrives as a parameter is the number of bits

        Returns:
            function lambda: calculates the size of bits and stops them in string
        """
        human_readable_size = lambda sbytes: (
            f"{sbytes} B"
            if sbytes < 1024
            else (
                f"{sbytes / 1024:.2f} KB"
                if sbytes < 1024**2
                else (
                    f"{sbytes / (1024 ** 2):.2f} MB"
                    if sbytes < 1024**3
                    else f"{sbytes / (1024 ** 3):.2f} GB"
                )
            )
        )
        return human_readable_size(sbytes)

    def _file_utils(self, jsonpath: str, option: str, objects=None) -> dict | None:
        """The `file_utils` method is only responsible for downloading and reading the json file,
        where it will be saved in the path declared in the `self.__path_file_json_zig` variable.

        Args:
            jsonpath (str): file download and save path
            option (str): the option that the open method will carry, either for example writing or reading (w, r)
            objects (optional): The optional parameter will only be added in case you want to write. Defaults to None.

        Returns:
            dict | None
        """
        match option:
            case "w":
                with open(jsonpath, option) as json_file:
                    json_file.write(objects)
            case "r":
                with open(jsonpath, option) as json_file:
                    data = json.load(json_file)
                return data
            case _:
                raise ValueError("Option must be 'w' (write) or 'r' (read)")

    def _download_json(self) -> int:
        """
        This method performs a GET request to the provided URL
        and saves the response JSON to a file named "zigreleses.json".

        Returns:
            int: 0 indicating success, 1 indicating error
        """
        try:
            response = requests.get(self._url)
            if response.status_code == 200:
                self._file_utils(self._path_file_json_zig, "w", response.text)
                return 0
            else:
                print(
                    f"[!] The request was not successful, error code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            print(f"Error when making request: {e}")

        return 1

    def list_release_zig(self) -> None:
        """
        only lists zig versions
        """
        if not os.path.exists(self._path_file_json_zig):
            if self._download_json() == 0:
                pass
            else:
                pass
        else:
            data: dict = self._file_utils(self._path_file_json_zig, "r")
            print(f"{'Version':>15} {'Date':>7}\n")
            for i, (version, _) in enumerate(data.items()):
                print(
                    f"{c.green(f'[{i}]'):<10} \t{version:<10} {data[version]['date']:<10}"
                )
            exit(0)

    def info_version(self, version: str) -> None:
        """This method aims to make several plots,
        showing in a pleasant way the output of the binary links and release dates.

        Args:
            version (str): the version comes as a parameter from argparse as a string
        """
        data: dict = self._file_utils(self._path_file_json_zig, "r")
        version_releases = [k for k, _ in data.items()]
        if version in version_releases:
            print(f"Details for version: {c.green(version):>10}\n")

            # print the details for a specific version
            for k, v in data[version].items():
                if isinstance(v, dict):
                    print(f"{c.green(k)}:")
                    for sub_k, sub_v in v.items():
                        if sub_k == "size":
                            sub_v = self._human_size_utils(int(sub_v))
                        print(f"  {c.yellow(sub_k)}: {sub_v}")
                else:
                    print(f"{c.green(k)}: {v}")
        else:
            print(f"Version [{c.red(version)}] not found.")
            print(
                f"{c.cyan(f"Use: {os.path.basename(__file__)} -h or --help for more info")}"
            )  # check path file `os.path.basename(__file__)`



def arg_parse() -> argparse.Namespace:
    parse = argparse.ArgumentParser(
        description="Download and update zig versions", usage="zigupdate [args]"
    )
    parse.add_argument("--version", "-v", help="prints the version and ends with a successful output 0", action="store-true")
    parse.add_argument(
        "--list-releases",
        "-lr",
        help="brings all available versions of zig",
        action="store_true",
    )
    parse.add_argument(
        "--info-version", "-iv", help="prints the information of a specific version"
    )
    return parse.parse_args()


def main() -> None:
    argv = arg_parse()
    rpz: RequestPageZig = RequestPageZig()

    if argv.list_releases:
        rpz.list_release_zig()
    elif argv.info_version:
        rpz.info_version(argv.info_version)


if __name__ == "__main__":
    main()
