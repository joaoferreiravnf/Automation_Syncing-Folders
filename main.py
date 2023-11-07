from sync import Synchronization
import datetime
import time
import os

def start():

    print('\nGreatings! This is your Syncronization App. Please specify the following:\n')
    while True:
        original_path = input('Please input the complete path of the folder you wish to be backed up: \n')
        if os.path.isdir(original_path):
            break
        else:
            print('The path given is invalid. Please try again.')
    while True:
        replica_path = input('\nPlease input the complete path of the folder where you wish to keep the copied files: \n')
        if os.path.isdir(replica_path):
            break
        else:
            print('The path given is invalid. Please try again.')
    while True:
        log_path = input('\nPlease input the complete path of the file where you wish to keep the log file: \n')
        if os.path.isfile(log_path):
            break
        else:
            print('The path given is invalid. Please try again.')
    while True:
        sync_interval = input('\nPlease input the time interval (in seconds) that you wish the app to syncronize: \n')
        if sync_interval.isnumeric() and int(sync_interval) > 0:
            break
        else:
            print('The value given is invalid. Please try again.')

    if __name__ == '__main__':
        write_initial_log = open(log_path, 'a')
        write_initial_log.write(f'\nSyncronization started at {datetime.datetime.now()}\n')
        write_initial_log.close()
        print(f'\nSyncronization started at {datetime.datetime.now()}\n')

        while True:

            syncer = Synchronization(original_path, replica_path, log_path, sync_interval)
            syncer.sync()
            syncer.compare_copy_files(syncer.replica_path, syncer.original_files, syncer.replica_files, syncer.log_path)
            syncer.remove_files(syncer.original_files, syncer.replica_files, syncer.log_path)
            time.sleep(int(sync_interval))

    write_initial_log = open(log_path, 'a')
    write_initial_log.write(f'\nSyncronization stopped at {datetime.datetime.now()}\n')
    write_initial_log.close()

start()


