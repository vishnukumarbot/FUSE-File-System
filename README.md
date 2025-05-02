# 📁 FUSE Virtual File System with Metadata, Cloud Sync & LFU Caching

## Description
This project implements a virtual file system using **FUSE (Filesystem in Userspace)** in Python. Features include:

- 🗃️ **MySQL-based Metadata Storage**
- ☁️ **Google Drive Cloud Sync** with deduplication & async syncing
- ⚡ **LFU (Least Frequently Used) Cache** to optimize reads

## Project Structure

```bash
FuseFS/
- fuse_main.py              # Main FUSE implementation
- mysql_code.py             # MySQL connection and operations
- lfu_cache.py              # LFU caching mechanism
- test_google_drive.py      # Google Drive sync logic
- requirements.txt          # Dependencies
- README.md                 
```

---

## Prerequisites

Ensure you have the following installed:

```bash
sudo apt update
sudo apt install fuse
pip install -r requirements.txt
```

---

##  Setup

### 1. MySQL Database

1. Start MySQL server:
   ```bash
   sudo service mysql start
   ```

### 2. Google Drive API Setup

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Go to IAM
- Check for service account
- Create the key for service account
- Once key is created you will get download json option
- Download `security.json` and place it in the project root
- Share the Google drive folder editor access to that service account.

---

## Run the Virtual File System

```bash
mkdir ~/fuse_mount  #Folder creation
py fuse_main.py ~/fuse_mount
```

To unmount:
```bash
fusermount -u ~/fuse_mount
```

---

##  Features Summary

| Feature           | File                   | Description                                                                                      |
|-------------------|------------------------|--------------------------------------------------------------------------------------------------|
| FUSE              | `fuse_main.py`         | Handles mount, read, write, delete                                                              |
| MYSQL DB          | `metadata_db.py`       | MySQL for storing metadata file paths, timestamps, size, hashes                                 |
| Google Sync       | `test_google_drive.py` | Async uploads to Google Drive with deduplication                                                |
| LFU Cache         | `lfu_cache.py`         | Keeps least frequently accessed files, shows items in cache and also shows content of text files|
| Read performance  || `performance_code.py` | Shows the read performance of a file                                                            | 
---

---

##  Testing

```bash
# Basic file creation
touch ~/fuse_mount/testfile.txt

# Write data
echo "Hello FUSE!" > ~/fuse_mount/testfile.txt

# Check MySQL for metadata and Google Drive for logs uploaded by running below commands
py mysql_code.py
py test_google_drive.py
py lfu_cache.py
py performance_code.py
```
