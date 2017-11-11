from setuptools import setup, find_packages

setup(name='simple_bank_korea',
      version='0.2.9',
      url='https://github.com/beomi/simple_bank_korea',
      license='MIT',
      author='Junbum Lee',
      author_email='jun@beomi.net',
      description='Crawling Korea bank transactions',
      packages=find_packages(),
      long_description="""\
      Crawler with requests/bs4/selenium/PhantomJS for Korea Bank Transctions.
      Currently supports Kookmin Bank""",
      zip_safe=False,
      setup_requires=['python-dateutil', 'requests', 'bs4', 'selenium', 'pillow'],
      install_requires=['python-dateutil', 'requests', 'bs4', 'selenium', 'pillow'],
      download_url='https://github.com/beomi/simple_bank_korea/archive/0.2.9.tar.gz',
      include_package_data = True,
      )
