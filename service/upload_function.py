import hashlib
import time
import calendar
import os
import mysql
import dbconfig
from pathlib import Path
from utility.process_yaml import get_parameters
import shutil


class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):

    def _float32_to_mysql(self, value):
        return float(value)

    def _float64_to_mysql(self, value):
        return float(value)

    def _int32_to_mysql(self, value):
        return int(value)

    def _int64_to_mysql(self, value):
        return int(value)


def get_checksum(path, file_name):
    file_path = path + '\\' + file_name
    h = hashlib.sha1()
    with open(file_path, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()


def save_paper_details(isthisFile, jsondatavalue):
    connection = dbconfig.connect()
    connection.set_converter_class(NumpyMySQLConverter)
    mycursor = connection.cursor(buffered=True)
    ts = str(calendar.timegm(time.gmtime()))
    original_filename = isthisFile.filename
    extension = isthisFile.filename.split(".")[-1]
    if extension not in get_parameters()['allowed_formats']:
        return 'Invalid file type', 400, None
    file_name = jsondatavalue['subjectName'] + "_" + ts + "." + extension
    mycursor.execute('select pd_original_file_name from paper_details where pd_original_file_name= %s',
                     (original_filename,))
    cnt = mycursor.rowcount
    if cnt > 0:
        return 'FileName already exists, try renaming the file and upload again', 400, None
    original_file_dir = 'FILES/' + jsondatavalue['path'] + '/ORIGINAL'
    if not os.path.exists(original_file_dir):
        os.makedirs(original_file_dir)
    isthisFile.save(os.path.join(original_file_dir, original_filename))
    original_file_path = original_file_dir + '\\' + original_filename
    file_size = float(Path(original_file_dir + '\\' + original_filename).stat().st_size)
    if file_size > float(get_parameters()['file_size']):
        os.remove(original_file_path)
        return 'File exceeds the allowed file size', 400, None
    file_dir = 'FILES/' + jsondatavalue['path'] + '/FINAL'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    newPath = shutil.copy(original_file_path, file_dir)
    file_path = file_dir + '\\' + file_name
    os.rename(file_dir + '\\' + original_filename, file_path)
    checksum_value = get_checksum(original_file_dir, original_filename)
    mycursor.execute('select pd_file_checksum from paper_details where pd_file_checksum= %s',
                     (checksum_value,))
    cnt = mycursor.rowcount
    file_path = file_dir + '\\' + file_name
    if cnt > 0:
        os.remove(original_file_path)
        os.remove(file_path)
        return 'File already exists', 400, None
    user_id = jsondatavalue['userId']
    sql = 'INSERT INTO paper_details(pd_original_file_name,pd_original_file_path,pd_file_name,pd_file_path,pd_file_checksum,pd_created_by,pd_updated_by)' \
          ' VALUES (%s, %s, %s, %s, %s, %s, %s)'
    mycursor.execute(sql, (
        original_filename, original_file_path, file_name, file_path,
        checksum_value, user_id, user_id))
    mycursor.execute("commit")
    return 'File uploaded successfully', 200, None
