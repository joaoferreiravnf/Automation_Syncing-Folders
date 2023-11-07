import os
import shutil
import hashlib
import datetime

class Synchronization:

    original_files = []
    replica_files = []

    def __init__(self, original_path, replica_path, log_path, sync_interval):        
        self.original_path = original_path
        self.replica_path = replica_path
        self.log_path = log_path
        self.sync_interval = sync_interval

    # Defining a hash value to every file in the original folder
    def hash_files(self, path):

        self.path = path

        buf_size = 65536
        md5 = hashlib.md5()

        try:
            with open(path, 'rb') as f:
                data = f.read(buf_size)
                md5.update(data)
        except IOError as hash_error:
            print(f"The following error occurred while reading the file: {hash_error}")
        return md5.hexdigest()

    # Reading all the files from each folder to then compare them
    def lookup_files(self, bigdirectory, files):

        def lookup_files_inside(smalldirectory, files):    

            for file in os.scandir(smalldirectory):
                try:
                    if file.is_file():
                        files.append({
                            'Name' : file.name,
                            'Path' : file.path,
                            'Relative Path' : os.path.dirname(os.path.relpath(file.path, bigdirectory)),
                            'Hash' : self.hash_files(file.path),
                            'Folder' : False})
                    elif file.is_dir():
                        files.append({
                            'Name' : file.name,
                            'Path' : file.path,
                            'Relative Path' : os.path.dirname(os.path.relpath(file.path, bigdirectory)),
                            'Hash' : os.path.relpath(file.path, bigdirectory),
                            'Folder' : True})
                        if len(os.listdir(file.path)) != 0:
                            lookup_files_inside(file.path, files)

                except OSError as lookup_error:
                    print(f'An error occured while searching: {lookup_error}')

        lookup_files_inside(bigdirectory, files)

    def sync(self):
        self.original_files.clear()
        self.replica_files.clear()

        self.lookup_files(self.original_path, self.original_files)
        self.lookup_files(self.replica_path, self.replica_files)

    # Comparing all the files and then copying the ones missing
    def compare_copy_files(self, replica_path, original_files, replica_files, log_path):

        write_log_copy = open(log_path, 'a')
        files2_info = {(file2['Name'], file2['Hash'], file2['Relative Path'], file2['Folder']) for file2 in replica_files}

        for file1 in original_files:
            
            target_path = os.path.join(replica_path, file1['Relative Path'])
            target_file_path = os.path.join(target_path, file1['Name'])
            write_copy_log_text = f'\nFile \"{file1["Name"]}\" copied from {file1["Path"]} to {target_file_path} at {datetime.datetime.now()}'

            if (file1['Name'], file1['Hash'], file1['Relative Path'], file1['Folder']) in files2_info: 
                continue
            else:            
                try:
                    os.makedirs(target_path, exist_ok=True)

                    if file1['Folder'] == False:
                        shutil.copy2(file1['Path'], target_file_path)
                        write_log_copy.write(write_copy_log_text)
                        print(write_copy_log_text)
                    else:
                        os.makedirs(target_file_path)
                        write_log_copy.write(write_copy_log_text)
                        print(write_copy_log_text)
                        
                except OSError as copy_error:
                    print(f'An error occured while copyng {file1}: {copy_error}')              

        write_log_copy.close()
            
    # Comparing all the files and then removing the ones not in the original folder
    def remove_files(self, original_files, replica_files, log_path):

        writelog_remove = open(log_path, 'a')

        for file2 in replica_files:

            files1_info = {(file1['Name'], file1['Hash'], file1['Relative Path']) for file1 in original_files}
            write_remove_log_text = f'File {file2["Name"]} with the path {file2["Path"]} has been removed at {datetime.datetime.now()}.'

            if (file2['Name'], file2['Hash'], file2['Relative Path']) not in files1_info:
                if file2['Folder'] == False:
                    try:
                        os.remove(file2['Path'])
                        writelog_remove.write(write_remove_log_text)
                        print(write_remove_log_text)
                    except FileNotFoundError:
                        print(f"File {file2['Name']} has already been removed or doesnt exist.")
                else:
                    try:
                        shutil.rmtree(file2['Path'])
                        writelog_remove.write(write_remove_log_text)
                        print(write_remove_log_text)
                    except OSError as remove_error:
                        print(f"It wasnt possible to remove {file2['Name']} because of: {remove_error}")

        writelog_remove.close()