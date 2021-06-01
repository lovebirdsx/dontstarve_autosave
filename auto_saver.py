from save_snapshot import SaveSnapshot
from backup_dir import BackupDir

class AutoSaver:

    def __init__(self, save_dir, backup_dir, max_backup):
        self.backup_dir = BackupDir(backup_dir, max_backup)
        self.save_dir = save_dir
        self.is_backuping = False

    def need_backup(self) -> bool:
        ss = SaveSnapshot(self.save_dir)
        return not self.backup_dir.has_snapshot(ss)
    
    def try_backup(self):
        if self.is_backuping:
            print('is backuping, no need run again')
            return

        self.is_backuping = True
        ss = SaveSnapshot(self.save_dir)
        if not self.backup_dir.has_snapshot(ss):
            self.backup_dir.add_snapshot(ss)
        self.is_backuping = False

    def restore(self, save_id:int):
        self.backup_dir.restore(save_id, self.save_dir)

    def remove(self, save_id:int):
        self.backup_dir.remove(save_id)
