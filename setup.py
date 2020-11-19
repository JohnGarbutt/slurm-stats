from setuptools import setup

setup(name='slurm-stats',
      version='0.1',
      description='Transforms slurm sacct output into json',
      url='https://github.com/JohnGarbutt/slurm-stats',
      author='John Garbutt',
      author_email='john.garbutt@stackhpc.com',
      license='Apache 2.0',
      packages=[],
      scripts=["sacct.py"],
      install_requires=["ClusterShell"],
      zip_safe=False)
