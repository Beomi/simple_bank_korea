import os
import platform
import tempfile
import zipfile
import tarfile
import requests

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

TMP_DIR = '/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir()


def get_phantomjs_path():
    # Download Phantomjs Binary if not exist
    def download_phantomjs(filename):
        # Download PhantomJS Binary
        file_path = os.path.join(TMP_DIR, filename)
        if not os.path.exists(file_path):
            response = requests.get(phantomjs_url, stream=True)
            f = open(file_path, "wb+")
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.close()
        return file_path

    if not os.path.exists(os.path.join(TMP_DIR, 'tmp')):
        os.makedirs(os.path.join(TMP_DIR, 'tmp'))
    try:
        # Check 'phantomjs' in Executable PATH
        webdriver.PhantomJS()
        return 'phantomjs'
    except WebDriverException as e:
        # No 'phantomjs' in PATH
        if not 'PATH' in str(e):
            raise e
        os_name = platform.system()
        if os_name.lower() == 'windows':
            phantomjs_url = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip'
            filename = 'phantomjs-2.1.1-windows.zip'
            file_path = download_phantomjs(filename)
        elif os_name.lower() == 'linux':
            phantomjs_url = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2'
            filename = 'phantomjs-2.1.1-linux-x86_64.tar.bz2'
            file_path = download_phantomjs(filename)
        elif os_name.lower() == 'darwin':
            phantomjs_url = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip'
            filename = 'phantomjs-2.1.1-macosx.zip'
            file_path = download_phantomjs(filename)
        else:
            raise Exception('Currently, Automatic phantomjs download does not supported in "{}" OS.\n'
                            'You can download and add phantomjs to PATH on your own,\n'
                            'Download Link: http://phantomjs.org/download.html'.format(os_name))

        if filename.endswith('zip'):
            foldername = filename.replace('.zip', '')
            file = zipfile.ZipFile(file_path)
            try:
                file.extract(foldername + '/bin/phantomjs', TMP_DIR)
                return os.path.join(TMP_DIR, 'phantomjs')
            except KeyError as e:
                if not 'windows' in str(e):
                    raise e
                file.extract(foldername + '/bin/phantomjs.exe', TMP_DIR)
                return os.path.join(TMP_DIR, 'phantomjs.exe')
        elif filename.endswith('tar.bz2'):
            foldername = filename.replace('.tar.bz2', '')
            file = tarfile.open(file_path, 'r:bz2')
            file.extract(foldername + '/bin/phantomjs', TMP_DIR)
            return os.path.join(TMP_DIR, 'phantomjs')
        else:
            raise Exception('File Name is not zip or tar.bz2')


if __name__ == '__main__':
    print('Result: ', get_phantomjs_path())
