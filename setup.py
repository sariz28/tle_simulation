from setuptools import setup, find_packages

setup(
    name="tle-simulacion",
    version="0.0.1",
    author="Sara Sanchez",
    author_email="sariz.sanchez@gmail.com",
    description="TLE Simulation",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages("modules/tle-simulation/src"),
    package_dir={"": "modules/tle-simulation/src"},
    python_requires='>=2.7,!=3.0.*,!=3.1.*'
)
