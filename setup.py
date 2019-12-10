import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

DEPENDENCIES = open('requirements.txt', 'r').read().split('\n')

setuptools.setup(
    include_package_data=True,
    name='rsolver',
    version='0.0.7',
    scripts=['rsolver/gui/rsolver'],
    author="Jeremías Pretto - Facundo Basso",
    author_email="jpretto@cert.unlp.edu.ar",
    description="CTF Solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/puckk",
    packages=['rsolver'],
    package_data={"": ["rsolver/scripts/*.py"]},
    install_requires=DEPENDENCIES,
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
