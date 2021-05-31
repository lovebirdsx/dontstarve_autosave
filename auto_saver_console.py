from save_snapshot import SaveSnapshot
import traceback
from auto_saver import AutoSaver

SaveDir = "C:/Program Files (x86)/Steam/userdata/86790013/219740/remote"
BackupDir = "C:/Users/lovebirdsx/OneDrive/work/game/save/Dont Starve"
BackupInterval = 60
MaxBackupCount = 10

def run():
    saver = AutoSaver(SaveDir, BackupDir, MaxBackupCount, BackupInterval)
    while True:
        v = input('[l] -> list [r] -> restore [s] -> start: ')
        if v == 's':
            saver.run()
        elif v == 'l':
            print(f'game dir: {saver.save_dir}')
            game_ss = SaveSnapshot(saver.save_dir)
            print(f'  {game_ss.name}')

            print(f'backups: max({saver.backup_dir.max_backup}) interval({saver.backup_interval}) {saver.backup_dir.dir}')
            snapshorts = saver.backup_dir.snapshots
            for i in range(len(snapshorts)):
                ss = snapshorts[i]
                print(f'  [{i}] {ss.name}')
        elif v == 'r':
            id_str = input('input the id your want to resotre: ')
            id = int(id_str)
            saver.restore(id)
        elif v == '':
            break
        else:
            print(f'unkown command [{v}]')

if __name__ == '__main__':
    try:
        run()
    except:
        traceback.print_exc()
        input('press enter to exist')
