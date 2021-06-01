import time
import threading
import PySimpleGUI as sg

from auto_saver import AutoSaver
from auto_saver_config import AutoSaverConfig

def init():
    global config
    global saver
    config = AutoSaverConfig()
    saver = AutoSaver(config.save_dir, config.backup_dir, config.max_backup_count)

def update_saver():
    global saver
    saver = AutoSaver(config.save_dir, config.backup_dir, config.max_backup_count)

def backup_thread(window:sg.Window):
    window['running_status'].update('backuping is running...')
    while True:
        if saver.need_backup():
            time.sleep(3)
            result = saver.try_backup()
            window.write_event_value('backuped', ('result', result))
        time.sleep(config.backup_interval)

def start(window:sg.Window):
    window['start'].update(disabled=True)
    window['save_dir'].update(disabled=True)
    window['backup_dir'].update(disabled=True)
    window['backup_interval'].update(disabled=True)
    window['max_backup_count'].update(disabled=True)
    window['save_dir_browse'].update(disabled=True)
    window['backup_dir_browse'].update(disabled=True)
    update_saver()
    threading.Thread(target=backup_thread, args=(window,), daemon=True).start()

def refresh(window:sg.Window, values):
    ss_cb = window['select_snapshot']
    snapshot_list = saver.backup_dir.snapshots_list
    ss_cb.update(values=snapshot_list)

    ss = values['select_snapshot']
    if ss not in snapshot_list:
        ss_cb.update(snapshot_list[0])
    else:
        ss_cb.update(ss)

    window['save_name'].update(f'Saved version: {saver.save_name}')

def backuped(window:sg.Window, values:dict):
    result = values['backuped'][1]
    if result is not None:
        window['running_status'].update(f'backup save to {result}')
        refresh(window, values)

def backup(window:sg.Window, values:dict):
    result = saver.try_backup()
    if result is not None:
        window['result'].update(f'backup {result} succeed')
        refresh(window, values)
    else:
        window['result'].update(f'backup {saver.save_name} falied')

def remove(window:sg.Window, values):
    ss = values['select_snapshot']
    if sg.popup_yes_no(f'Do you really want to remove {ss}?') == 'Yes':
        if saver.remove_by_name(ss):
            window['result'].update(f'remove {ss} succeed')
            refresh(window, values)
        else:
            window['result'].update(f'remove {ss} falied')


def restore(window:sg.Window, values):
    ss = values['select_snapshot']
    if sg.popup_yes_no(f'Do you really want to restore {ss}?') == 'Yes':
        if saver.restore_by_name(ss):
            window['result'].update(f'restore {ss} succeed')
            refresh(window, values)
        else:
            window['result'].update(f'restore {ss} failed')

def run():
    layout = [
        [
            sg.Text('Save dir', size=(10, 1)),
            sg.Input(size=(76, 1), enable_events=True, key='save_dir', default_text=config.save_dir),
            sg.FolderBrowse(initial_folder=config.save_dir, key='save_dir_browse')
        ],
        [
            sg.Text('Backup dir', size=(10, 1)),
            sg.In(size=(76, 1), enable_events=True, key='backup_dir', default_text=config.backup_dir),
            sg.FolderBrowse(initial_folder=config.backup_dir, key='backup_dir_browse')
        ],
        [
            sg.Text('Backup interval'),
            sg.In(size=(5, 1), enable_events=True, key='backup_interval', default_text=config.backup_interval),
            sg.Text('Max backup count'),
            sg.In(size=(5, 1), enable_events=True, key='max_backup_count', default_text=config.max_backup_count),
            sg.Button(button_text='Start', enable_events=True, key='start'),
        ],
        [
            sg.Text(f'Saved version: {saver.save_name}', key='save_name'),
            sg.Button(button_text='Backup', enable_events=True, key='backup'),
            sg.Button(button_text='Refresh', enable_events=True, key='refresh'),
            sg.Combo(values=saver.backup_dir.snapshots_list, enable_events=True, key='select_snapshot', default_value=saver.backup_dir.snapshots_list[0]),
            sg.Button(button_text='Remove', enable_events=True, key='remove'),
            sg.Button(button_text='Restore', enable_events=True, key='restore'),
        ],
        [
            sg.Text('Status: '),
            sg.Text('Click start to run backup thread', key='running_status', size=(30, 1)),
            sg.Text('Result: '),
            sg.Text('', key='result', size=(30, 1)),
        ],
    ]

    window = sg.Window('Don\'t Starve Auto Saver', layout)

    while True:
        ev, values = window.read()
        if ev == 'Exit' or ev == sg.WIN_CLOSED:
            break
        elif ev == 'save_dir':
            config.save_dir = values['save_dir']
        elif ev == 'backup_dir':
            config.backup_dir = values['backup_dir']
        elif ev == 'backup_interval':
            config.backup_interval = values['backup_interval']
        elif ev == 'max_backup_count':
            config.max_backup_count = values['max_backup_count']
        elif ev == 'start':
            start(window)            
        elif ev == 'refresh':
            refresh(window, values)
        elif ev == 'backup':
            backup(window, values)
        elif ev == 'backuped':
            backuped(window, values)
        elif ev == 'remove':
            remove(window, values)
        elif ev == 'restore':
            restore(window, values)
    window.close()

if __name__ == '__main__':
    init()
    run()
