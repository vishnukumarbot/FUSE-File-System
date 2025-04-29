# 📁 FUSE Virtual File System with Metadata, Cloud Sync & LFU Caching

## Description
This project implements a virtual file system using **FUSE (Filesystem in Userspace)** in Python. Features include:

- 🗃️ **MySQL-based Metadata Storage**
- ☁️ **Google Drive Cloud Sync** with deduplication & async syncing
- ⚡ **LFU (Least Frequently Used) Cache** to optimize reads
- 🔒 Authenticated access and performance benchmarks


## Project Structure

```bash
FuseFS/
- fuse_main.py             # Main FUSE implementation
- mysql_code.py           # MySQL connection and operations
- lfu_cache.py             # LFU caching mechanism
- test_google_drive.py       # Google Drive sync logic
- requirements.txt           # Dependencies
- README.md                 # This file
```

---

## 🔧 Prerequisites

Ensure you have the following installed:

```bash
sudo apt update
sudo apt install fuse
pip install -r requirements.txt
```

---

## 🛠️ Setup

### 1. MySQL Database

1. Start MySQL server:
   ```bash
   sudo service mysql start
   ```

2. Import database schema (if `schema.sql` provided):
   ```bash
   mysql -u <user> -p < schema.sql
   ```

### 2. Google Drive API Setup

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create OAuth2 credentials
- Download `credentials.json` and place it in the project root
- On first run, a browser window will open to authenticate.

---

## 🚀 Run the Virtual File System

```bash
mkdir ~/fuse_mount
python3 fuse_main.py ~/fuse_mount
```

To unmount:
```bash
fusermount -u ~/fuse_mount
```

---

## 🔁 Features Summary

| Feature           | File                  | Description                                      |
|------------------|-----------------------|--------------------------------------------------|
| FUSE Interface    | `fuse_main.py`         | Handles mount, read, write, delete               |
| Metadata DB       | `metadata_db.py`       | MySQL for file paths, timestamps, size, hashes   |
| Cloud Sync        | `gdrive_sync.py`       | Async uploads to Google Drive with deduplication |
| LFU Cache         | `cache_lfu.py`         | Keeps frequently accessed files in RAM           |

---

## 📊 Metrics Tracked

- **Throughput (MB/s)**
- **Cache Hit Ratio (%)**
- **Sync Success Rate (%)**

Tools: `UserBenchmark`, `custom logger`

---

## 🧪 Testing

```bash
# Basic file creation
touch ~/fuse_mount/testfile.txt

# Write data
echo "Hello FUSE!" > ~/fuse_mount/testfile.txt

# Check metadata and Google Drive upload logs
```

---
