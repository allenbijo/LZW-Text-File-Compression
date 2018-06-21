from distutils.core import setup

setup(name='lzw',
      version='0.2.0',
      description='utf-8 text file compression',
      author='Prathamesh Mandke',
      author_email='prathrules@gmail.com',
      packages=['lzw'],
      license='LICENSE.md',
      install_requires=['os','datetime','time'],
      long_description=open('README.md').read()
     )
