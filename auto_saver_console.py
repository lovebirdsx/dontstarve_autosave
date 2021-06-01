from auto_saver_config import AutoSaverConfig
from auto_saver_thread import AutoSaverThread
from save_snapshot import SaveSnapshot
import traceback
from auto_saver import AutoSaver

def run():
    try:
        config = AutoSaverConfig()
        saver = AutoSaver(config.save_dir, config.backup_dir, config.max_backup_count)
        saver_thread = AutoSaverThread(saver, config.backup_interval)
        saver_thread.start()
        while True:
            v = input('[i]nfo [b]ackup [r]estore [d]elete [e]xit: ')
            if v == 'i':
                print(f'game dir: {saver.save_dir}')
                game_ss = SaveSnapshot(saver.save_dir)
                print(f'  {game_ss.name}')

                print(f'backups: max({saver.backup_dir.max_backup}) interval({saver_thread.backup_interval}) {saver.backup_dir.dir}')
                snapshorts = saver.backup_dir.snapshots
                for i in range(len(snapshorts)):
                    ss = snapshorts[i]
                    print(f'  [{i}] {ss.name}')
            elif v == 'b':
                if saver.need_backup():
                    saver.try_backup()
                else:
                    print('nothing to backup')
            elif v == 'r':
                id_str = input('input the id your want to resotre: ')
                id = int(id_str)
                saver.restore(id)
            elif v == 'd':
                id_str = input('input the id your want to delete: ')
                id = int(id_str)
                saver.remove(id)
            elif v == 'e':
                saver_thread.stop()
                input('press enter to exist')
                break
            else:
                print(f'unkown command [{v}]')
    except:
        traceback.print_exc()
        saver_thread.stop()
        input('press enter to exist')

if __name__ == '__main__':
    run()
