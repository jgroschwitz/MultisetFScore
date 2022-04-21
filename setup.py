import setuptools

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
     name='multiset_fscore',
     version='1.0',
     scripts=[] ,
     author="Jonas Groschwitz",
     description="Code to calculate the multiset F-score of token sequences",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/jgroschwitz/multisetfscore",
     packages=setuptools.find_packages(
         where='.',
         include=['multiset_fscore.py'],  # empty by default
     ),
     classifiers=[
         "Programming Language :: Python :: 3",
     ],

 )