import os
import platform
import tempfile
import zipfile
import tarfile
import requests

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from tqdm import tqdm

TMP_DIR = '/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir()


def get_phantomjs_path(phantomjs_path=None):
    # if phantomjs_path is provided, use it as PATH
    if phantomjs_path:
        return phantomjs_path

    # Download Phantomjs Binary if not exist
    def download_phantomjs(filename):
        # Download PhantomJS Binary
        file_path = os.path.join(TMP_DIR, filename)
        if not os.path.exists(file_path):
            print("::Download PhantomJS::")
            response = requests.get(phantomjs_url, stream=True)
            f = open(file_path, "wb+")
            for chunk in tqdm(response.iter_content(chunk_size=1024)):
                if chunk:
                    f.write(chunk)
            f.close()
            print("::Download Finish::")
        return file_path

    if not os.path.exists(os.path.join(TMP_DIR, 'tmp')):
        os.makedirs(os.path.join(TMP_DIR, 'tmp'))
    try:
        # Check 'phantomjs' in Executable PATH
        webdriver.PhantomJS()
        return 'phantomjs'
    except WebDriverException as e:
        # No 'phantomjs' in PATH
        if 'PATH' not in str(e):
            raise e
        os_name = platform.system()
        if os_name.lower() == 'windows':
            print("::OS Detected - Windows::")
            phantomjs_url = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip'
            filename = 'phantomjs-2.1.1-windows.zip'
            file_path = download_phantomjs(filename)
        elif os_name.lower() == 'linux':
            print("::OS Detected - Linux::")
            phantomjs_url = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2'
            filename = 'phantomjs-2.1.1-linux-x86_64.tar.bz2'
            file_path = download_phantomjs(filename)
        elif os_name.lower() == 'darwin':
            print("::OS Detected - macOS::")
            phantomjs_url = 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip'
            filename = 'phantomjs-2.1.1-macosx.zip'
            file_path = download_phantomjs(filename)
        else:
            raise Exception('Currently, Automatic phantomjs download does not supported in "{}" OS.\n'
                            'You can download and add phantomjs to PATH on your own,\n'
                            'Download Link: http://phantomjs.org/download.html'.format(os_name))

        if filename.endswith('zip'):
            folder_name = filename.replace('.zip', '')
            file = zipfile.ZipFile(file_path)
            try:
                file.extract(folder_name + '/bin/phantomjs', TMP_DIR)
                phantom_path = os.path.join(TMP_DIR, folder_name + '/bin/phantomjs')
                os.chmod(phantom_path, 755)  # Fix permission
                return phantom_path
            except KeyError as e:
                if 'windows' not in str(e):
                    raise e
                file.extract(folder_name + '/bin/phantomjs.exe', TMP_DIR)
                return os.path.join(TMP_DIR, folder_name + '/bin/phantomjs.exe')
        elif filename.endswith('tar.bz2'):
            folder_name = filename.replace('.tar.bz2', '')
            file = tarfile.open(file_path, 'r:bz2')
            file.extract(folder_name + '/bin/phantomjs', TMP_DIR)
            phantom_path = os.path.join(TMP_DIR, folder_name + '/bin/phantomjs')
            os.chmod(phantom_path, 755)  # Fix permission
            return phantom_path
        else:
            raise Exception('File Name is not zip or tar.bz2')


if __name__ == '__main__':
    print('Result: ', get_phantomjs_path())
