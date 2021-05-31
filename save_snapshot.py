import os
import filetimes
from shutil import rmtree

class SaveSnapshot:

    def __init__(self, dir):
        self.dir = dir
        self.index_file = os.path.join(dir, "saveindex")
        self.time_stamp = os.stat(self.index_file).st_mtime
        self.time_stamp_dt = filetimes.FILETIME(self.time_stamp)

    def remove(self):
        print(f'remove: {self.dir}')
        rmtree(self.dir)
    
    @property
    def name(self):
        return str(self.time_stamp_dt)

if __name__ == "__main__":
    ss = SaveSnapshot("C:/Program Files (x86)/Steam/userdata/86790013/219740/remote")
    print(ss.time_stamp_dt)