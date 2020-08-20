import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()
    
setuptools.setup(
    name="python_heideltime",
    version=1.0,
    author="Philip Hausner",
    author_email="hausner@informatik.uni-heidelberg.de",
    description="Python wrapper for HeidelTime",
    long_description=long_description,
    url="https://github.com/PhilipEHausner/python_heideltime",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ;; OSI Approved :: GNU GPL",
        "Operating System :: Debian",
        ],
    python_requires='>=3.6',
    )
