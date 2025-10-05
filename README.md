# 🦎 zigchad

> **CLI script to easily manage and download Zig versions directly from your terminal.**  
> _"God Is First" — Created by [Jakepys](https://github.com/JuanPerdomo00)_

---

## 📦 Features

- 🔍 List all available Zig releases.
- ℹ️ Display detailed info of a specific version.
- ⬇️ Download and extract Zig versions by architecture.
- 💾 Stores the official Zig JSON file temporarily at `/tmp/.zigreleses.json`.
- 🌈 Colorful terminal output for readability.

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/JuanPerdomo00/zigchad.git
cd zigchad
```

### 2️⃣ Make it executable

```bash
chmod +x zigchad.py
```

### 3️⃣ Run

```bash
./zigchad.py --help
```

---

## 💡 Usage

### 📋 List all available releases

```bash
./zigchad.py --list-releases
```

### 🔎 Show detailed info for a specific version

```bash
./zigchad.py --info-version-zig 0.11.0
```

### ⬇️ Download a specific Zig version

```bash
./zigchad.py --download 0.11.0 x86_64-linux /home/user/Downloads
```

This will:
- Fetch Zig version `0.11.0`
- Download the `x86_64-linux` build
- Automatically extract it into `/home/user/Downloads`

---

## 🧠 Example output

```
Version: 0.11.0
Architecture: x86_64-linux
tarball: https://ziglang.org/download/0.11.0/zig-linux-x86_64-0.11.0.tar.xz
size: 44.2 MB

File downloaded successfully to: /home/user/Downloads/zig-0.11.0.tar.xz
Extracted in /home/user/Downloads
```

---

## 🔧 Available Arguments

| Option | Description |
|--------|--------------|
| `-v, --version` | Prints the script version. |
| `-lr, --list-releases` | Lists all available Zig releases. |
| `-ivz, --info-version-zig [version]` | Shows details about a specific version. |
| `-d, --download [version] [architecture] [path]` | Downloads and extracts a specific Zig build. |

---

## 🧩 Requirements

- Python ≥ 3.8  

---

## 🧑‍💻 Author

**Jakepys**  
- 🧠 GitHub: [@JuanPerdomo00](https://github.com/JuanPerdomo00)  
- ✝️ Motto: *God Is First*  

---

## ⚖️ License

This project is licensed under the **GNU GPLv3**.  
See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.html) for details.

---

## 🌟 Current Version

`zigchad v0.1.3`

---

## 💬 Quick Example

```bash
# Download Zig version 0.14.1 for Linux
./zigchad.py -d 0.14.1 x86_64-linux ~/Downloads
```

---

> _“Faith moves mountains, but code moves the world.”_  
> 🦎 **zigchad** — built with passion and purpose.
