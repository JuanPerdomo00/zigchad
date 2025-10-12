# 🦎 zigchad

CLI script to easily manage and download Zig versions directly from your terminal."God Is First" — Created by Jakepys


## 📦 Features

- 🔍 List all available Zig releases.
- ℹ️ Display detailed info for a specific version.
- ⬇️ Download and extract Zig versions by architecture.
- 🔗 Set a specific Zig version as active using a symbolic link.
- 🗑️ Remove installed Zig versions or temporary tar files.
- 📋 List installed Zig versions.
- 📁 Support for custom Zig installation directories.
- 💾 Stores the official Zig JSON file temporarily at /tmp/.zigreleases.json.


## ⚙️ Installation
```sh
# Clone the repository
git clone https://github.com/JuanPerdomo00/zigchad.git
cd zigchad

# Install dependencies
# Ensure you have Python ≥ 3.8 and the requests library installed:
# pip install requests
# our use uv 

# Make it executable
chmod +x zigchad.py

# Add Zig directory to PATH (optional)
# To use the zig command directly after setting a version with --use-version, add ~/.zig_versions to your PATH:
echo 'export PATH=$PATH:$HOME/.zig_versions' >> ~/.zshrc
source ~/.zshrc

# Replace ~/.zshrc with ~/.bashrc or your shell configuration file if needed.

#Run
./zigchad.py --help
```

## 💡 Usage
```sh
# 📋 List all available releases
./zigchad.py --list-releases

# 🔎 Show detailed info for a specific version
./zigchad.py --info-version-zig 0.13.0

# ⬇️ Download a specific Zig version
./zigchad.py --download 0.13.0 x86_64-linux ~/.zig_versions

This will:

Fetch Zig version 0.13.0
Download the x86_64-linux build
Automatically extract it into ~/.zig_versions/zig-0.13.0
Remove the downloaded tar file

# 🔗 Set an active Zig version
./zigchad.py --use-version 0.13.0

# This creates a symbolic link at ~/.zig_versions/zig pointing to ~/.zig_versions/zig-0.13.0/zig. If ~/.zig_versions is in your PATH, you can run:
zig --version

# 🗑️ Remove a specific Zig version
./zigchad.py --remove-version 0.13.0

# This deletes the ~/.zig_versions/zig-0.13.0 folder and removes the symbolic link if it points to this version.
# 📋 List installed Zig versions
./zigchad.py --list-versions-installed

# 🔄 Rename an installed Zig version
./zigchad.py --rename 0.13.0 my-zig-version

# Renames ~/.zig_versions/zig-0.13.0 to ~/.zig_versions/my-zig-version.
# 🗑️ Remove temporary tar files
./zigchad.py --removetar

# 📁 Use a custom Zig directory
# Use the --zig-dir option to specify a different directory for Zig versions:
./zigchad.py --zig-dir ~/.zig_installed --use-version 0.13.0
```
```sh
🧠 Example output
Downloading a version:
Version: 0.13.0
Architecture: x86_64-linux
Download Details:
------------------------------
tarball: https://ziglang.org/download/0.13.0/zig-linux-x86_64-0.13.0.tar.xz
size: 44.2 MB
shasum: 2d94984923...

File downloaded successfully to: /home/user/.zig_versions/zig-0.13.0.tar.xz
Extracted to: /home/user/.zig_versions
Renamed folder: /home/user/.zig_versions/zig-linux-x86_64-0.13.0 to /home/user/.zig_versions/zig-0.13.0
Removed tar file: /home/user/.zig_versions/zig-0.13.0.tar.xz

Setting a version as active:
Created symbolic link: /home/user/.zig_versions/zig -> /home/user/.zig_versions/zig-0.13.0/zig
You can now use zig by running: zig
```

## 🔧 Available Arguments

```sh
-v, --version
# Prints the script version (0.1.4).


-lr, --list-releases
# Lists all available Zig releases.


-ivz, --info-version-zig [version]
# Shows details about a specific version.


-d, --download [version] [architecture] [path]
# Downloads and extracts a specific Zig build.


-r, --rename [version] [new_name]
# Renames the folder of an installed Zig version.


-uv, --use-version [version]
# Sets the specified version as active by creating a symbolic link in zig_dir.


-rv, --remove-version [version]
# Removes the specified Zig version folder.


-lvi, --list-versions-installed
# Lists all installed Zig versions.


-rt, --removetar
# Removes all temporary .tar files from zig_dir.


--zig-dir [dir]
# Specifies the directory for Zig versions (default: ~/.zig_versions).
```

## 🧩 Requirements

- Python ≥ 3.8
- requests library (pip install requests) or use uv


## 🧑‍💻 Author
- Jakepys  

- 🧠 GitHub: @JuanPerdomo00  
- ✝️ Motto: God Is First


## ⚖️ License
This project is licensed under the GNU GPLv3.See LICENSE for details.

## 🌟 Current Version
zigchad v0.1.4

## 💬 Quick Example
## Download Zig version 0.13.0 for Linux
`./zigchad.py -d 0.13.0 x86_64-linux ~/.zig_versions`

# Set Zig version 0.13.0 as active
`./zigchad.py -uv 0.13.0`

# Verify
`zig version`


“Faith moves mountains, but code moves the world.”🦎 zigchad — built with passion and purpose.
