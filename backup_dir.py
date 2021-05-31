import os
from shutil import copytree, rmtree
import time
from save_snapshot import SaveSnapshot

class BackupDir:

    def __init__(self, dir, max_backup):
        self.dir = dir
        self.max_backup = max_backup
        self.snapshots = self.parse()
    
    def parse(self) -> list[SaveSnapshot]:
        names = os.listdir(self.dir)
        l = list()
        for name in names:
            l.append(SaveSnapshot(os.path.join(self.dir, name)))
        return l

    def has_snapshot(self, ss:SaveSnapshot) -> bool:
        ss0 = next((x for x in self.snapshots if x.time_stamp == ss.time_stamp), None)
        return ss0 != None

    def add_snapshot(self, ss:SaveSnapshot):
        src = ss.dir
        to = os.path.join(self.dir, str(ss.time_stamp_dt))
        print(f'backup {src} -> {to}')
        time.sleep(5)
        copytree(src, to)
        self.snapshots.append(SaveSnapshot(to))
        self.check_remove()

    def check_remove(self):
        self.snapshots.sort(key=lambda x: str(x.time_stamp_dt))
        while len(self.snapshots) > self.max_backup:
            ss0 = self.snapshots.pop(0)
            ss0.remove()

    def restore(self, id:int, dir:str):
        if id < 0 or id >= len(self.snapshots):
            print(f'no backup for id [{id}]')
            return
        
        ss = self.snapshots[id]
        print(f'restore {ss.dir} -> {dir}')
        rmtree(dir)
        copytree(ss.dir, dir)

    def output_info(self):
        print(f'base dir is {self.dir}')
        print(f'max backup count {self.max_backup}')
        print(f'current backup count {len(self.snapshots)}')
        print(f'backup list:')
        for ss in self.snapshots:
            print(f'  {ss.dir}')

if __name__ == '__main__':
    bd = BackupDir('C:/Users/lovebirdsx/OneDrive/work/game/save/Dont Starve', 10)
    bd.check_remove()
    bd.output_info()

    game_save_dir = 'C:/Program Files (x86)/Steam/userdata/86790013/219740/remote'
    ss = SaveSnapshot(game_save_dir)
    print(f'backupdir has {ss.time_stamp_dt} is {bd.has_snapshot(ss)}')

    if not bd.has_snapshot(ss):
        bd.add_snapshot(ss)

    print('backupdir info -----------------')
    bd.output_info()
