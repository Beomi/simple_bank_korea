from setuptools import setup, find_packages

setup(name='simple_bank_korea',
      version='0.2.11',
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
      setup_requires=[
            "bs4",
            "requests<2.19",
            "python-dateutil<2.7",
            "pillow<5",
            "selenium<3.7"
      ],
      install_requires=[
            "bs4",
            "requests<2.19",
            "python-dateutil<2.7",
            "pillow<5",
            "selenium<3.7"
      ],
      download_url='https://github.com/beomi/simple_bank_korea/archive/0.2.11.tar.gz',
      include_package_data = True,
      )
