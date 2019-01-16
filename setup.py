from distutils.core import setup

setup(name='lzw',
      version='2.0',
      description='utf-8 text file compression',
      author='Prathamesh Mandke',
      author_email='mandkepk97@gmail.com',
      packages=['lzw'],
      license='LICENSE.md',
      install_requires=['os','datetime','time'],
      url='https://github.com/pytholic97/LZW-Text-File-Compression',
      download_url='https://github.com/pytholic97/LZW-Text-File-Compression/tree/master/dist',
      long_description=open('README.md').read()
     )
