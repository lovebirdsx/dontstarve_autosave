from datetime import datetime
import time
from save_snapshot import SaveSnapshot
from backup_dir import BackupDir

class AutoSaver:

    def __init__(self, save_dir, backup_dir, max_backup, backup_interval):
        self.backup_dir = BackupDir(backup_dir, max_backup)
        self.backup_interval = backup_interval
        self.save_dir = save_dir

    def try_backup(self):
        ss = SaveSnapshot(self.save_dir)
        if not self.backup_dir.has_snapshot(ss):
            self.backup_dir.add_snapshot(ss)
        else:
            # print(f'{datetime.now().strftime("%Y%m%d-%H%M%S")} nothing to backup')
            pass

    def restore(self, save_id:int):
        self.backup_dir.restore(save_id, self.save_dir)

    def run(self):
        while True:
            time.sleep(self.backup_interval)
            self.try_backup()