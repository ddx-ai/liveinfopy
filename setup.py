from setuptools import setup, find_packages
from pathlib import Path

from live_info_api_client import __VERSION__ as VERSION


setup(
  name='live_info_api_client',

  # version example
  #   '0.1.0-alpha', # == 0.1.0-alpha0 == 0.1.0a0
  version=VERSION,

  license='MIT',

  packages=find_packages(),
  include_package_data=True,

  # entry_points = {
  #   'console_scripts': [
  #     # create `main` function in
  #     #   live_info_api_client/hoge.py
  #     'hoge = live_info_api_client.hoge:main',
  #   ],
  # },

  install_requires=(
    Path('requirements.in').read_text(encoding='utf-8').splitlines()
  ),

  author='aoirint',
  author_email='aoirint@gmail.com',

  url='https://github.com/aoirint/live_info_api_client_py',
  # description='SHORT_DESCRIPTION',

  long_description=Path('README.md').read_text(encoding='utf-8'),
  long_description_content_type='text/markdown',

  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
