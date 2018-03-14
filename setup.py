from setuptools import setup, find_packages

setup(name='tlushim',
      version='0.0.4',
      description='small tool to calculate your hours balance from the "Tlushim" site',
      author='Johnathan Viduchinsky and Yoav Ekshtein',
      url='https://github.com/johnathanvidu/tlushim',
      license='MIT License',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Programming Language :: Python :: 2.7',
                   'License :: OSI Approved :: MIT License'],
      packages=find_packages(exclude=['tests']),
      entry_points={'console_scripts': ['tlushim = tlushim.__main__:main']},
      install_requires=["requests==2.18.4", "beautifulsoup4==4.6.0"])
