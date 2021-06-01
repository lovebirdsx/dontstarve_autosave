import datetime
import threading
import time
from auto_saver import AutoSaver

class AutoSaverThread(threading.Thread):

    def __init__(self, saver:AutoSaver, backup_interval:int) -> None:
        super().__init__()
        self.saver = saver
        self.is_running = False
        self.backup_interval = backup_interval

    def run(self) -> None:
        self.is_running = True
        print(f'auto save thread start at {datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}')
        while self.is_running:
            if self.saver.need_backup():
                time.sleep(3)
                self.saver.try_backup()
            for _ in range(self.backup_interval):
                time.sleep(1)
                if not self.is_running:
                    break
        print(f'auto save thread stop at {datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}')

    def stop(self) -> None:
        self.is_running = False
        self.join()
