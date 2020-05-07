import os
import sys
import urllib.request
import shutil


def get_download_location():
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
    else:
        location = os.path.join(os.path.expanduser('~'), 'downloads')
    return location


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    return listOfFile


def download_papers(json_data):
    path_list = json_data['path']
    for path_data in path_list:
        path_data = path_data + '/FINAL/'
        download_location = get_download_location()
        listOfFileList = getListOfFiles(sys.path[0] + '/FILES/' + path_data)
        for listOfFile in listOfFileList:
            # urllib.request.urlretrieve('FILES/'+ path_data + '/' + listOfFile, download_location)
            shutil.copy('FILES/' + path_data + '/' + listOfFile, download_location)
    return 'Files downloaded succesfully', 200, None
