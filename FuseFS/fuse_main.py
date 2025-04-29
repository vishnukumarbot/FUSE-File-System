
import os
import fuse
from fuse import FUSE, Operations

class SimpleFS(Operations):
    def __init__(self):
        self.files = {'/hello.txt': 'Hello, world!'}
        
    def getattr(self, path):
        if path == '/':
            return {'st_mode': 16877, 'st_nlink': 2}  # Directory
        elif path in self.files:
            return {'st_mode': 33204, 'st_size': len(self.files[path]), 'st_nlink': 1}  # File
        else:
            raise fuse.FuseOSError(fuse.ENOENT)
    
    def readdir(self, path, fh):
        return ['.', '..'] + list(self.files.keys())
    
    def read(self, path, size, offset, fh):
        if path in self.files:
            return self.files[path][offset:offset + size]
        else:
            raise fuse.FuseOSError(fuse.ENOENT)
    
    def write(self, path, data, offset, fh):
        if path not in self.files:
            self.files[path] = ''
        self.files[path] = self.files[path][:offset] + data
        return len(data)

    def create(self, path, mode):
        if path in self.files:
            raise fuse.FuseOSError(fuse.EEXIST)
        self.files[path] = ''
        return self.files[path]

    def unlink(self, path):
        if path in self.files:
            del self.files[path]
        else:
            raise fuse.FuseOSError(fuse.ENOENT)

def main(mountpoint):
    FUSE(SimpleFS(), mountpoint, foreground=True)

if __name__ == "__main__":
    mountpoint = "/mnt/C/Path to Mount"  # Mount point 
    if not os.path.exists(mountpoint):
        os.makedirs(mountpoint)
    main(mountpoint)
