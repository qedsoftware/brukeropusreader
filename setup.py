from distutils.core import setup


setup(name='brukeropusreader',
      version='1.2.1',
      description='Bruker OPUS File Reader',
      author='QED',
      author_email='brukeropusreader-dev@qed.ai',
      packages=['brukeropusreader'],
      python_requires=">=3",
      install_requires=['numpy==1.13.3', 'scipy==0.19.1'],
      license="GPLv3",
      url="https://github.com/qedsoftware/brukeropusreader"
      )
