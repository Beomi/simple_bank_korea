from setuptools import setup, find_packages

setup(name='simple_bank_korea',
      version='0.1.0',
      url='https://github.com/beomi/simple_bank_korea',
      license='MIT',
      author='Junbum Lee',
      author_email='jun@beomi.net',
      description='Crawling Korea bank transactions',
      packages=find_packages(),
      long_description="""\
      Crawler with requests/bs4 for Korea Bank Transctions.
      Currently works with KB""",
      zip_safe=False,
      setup_requires=['python-dateutil', 'requests', 'bs4'],
      install_requires=['python-dateutil', 'requests', 'bs4'],
      download_url='https://github.com/beomi/simple_bank_korea/archive/0.1.0.tar.gz',
      )
