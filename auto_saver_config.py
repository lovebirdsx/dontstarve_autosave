from config import Config

SaveDir = 'C:/Program Files (x86)/Steam/userdata/86790013/219740/remote'
BackupDir = 'C:/Users/lovebirdsx/OneDrive/work/game/save/Dont Starve'
BackupInterval = 60
MaxBackupCount = 10

class AutoSaverConfig(Config):

    def __init__(self) -> None:
        super().__init__('auto_saver.json')
        self.save_dir
        self.max_backup_count
        self.backup_interval
        self.backup_dir
    
    @property
    def save_dir(self) -> str:
        return self.get('SaveDir', SaveDir)
    
    @save_dir.setter
    def save_dir(self, value) -> None:
        self.set('SaveDir', value)

    @property
    def backup_dir(self) -> str:
        return self.get('BackupDir', BackupDir)
    
    @backup_dir.setter
    def backup_dir(self, value) -> None:
        self.set('BackupDir', value)

    @property
    def backup_interval(self) -> int:
        return self.get('BackupInterval', BackupInterval)
    
    @backup_interval.setter
    def backup_interval(self, value) -> None:
        self.set('BackupInterval', int(value))

    @property
    def max_backup_count(self) -> int:
        return self.get('MaxBackupCount', MaxBackupCount)
    
    @max_backup_count.setter
    def max_backup_count(self, value) -> None:
        self.set('MaxBackupCount', int(value))

if __name__ == '__main__':
    config = AutoSaverConfig()
    print(config.save_dir)
    print(config.backup_dir)
    print(config.backup_interval)
    print(config.max_backup_count)
