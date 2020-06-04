from setuptools import setup, find_packages

REQ_FILE = 'requirements.txt'
VERSION = '0.2.15'

def get_requires():
    thisdir = os.path.dirname(__file__)
    reqpath = os.path.join(thisdir, REQ_FILE)
    return [line.rstrip('\n') for line in open(reqpath)]

setup(name='simple_bank_korea',
      version=VERSION,
      url='https://github.com/beomi/simple_bank_korea',
      license='MIT',
      author='Junbum Lee',
      author_email='jun@beomi.net',
      description='Crawling Korea bank transactions',
      packages=find_packages(),
      long_description=open('README.md', 'r', encoding="utf-8").read(),
      long_description_content_type="text/markdown",
      zip_safe=False,
      install_requires=get_requires(),
      include_package_data=True,
      classifiers=[
            "Programming Language :: Python :: 3",
      ],
)
