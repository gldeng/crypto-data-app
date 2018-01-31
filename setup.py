from setuptools import setup, find_packages
import os

this_dir = os.path.dirname(__file__)
install_requires = [
    x.strip() for x in open(os.path.join(this_dir, 'requirements.txt'))
    if x.strip()
]

setup(
    name="crypto-data-app" ,
    version="0.1.0" ,
    description="Crypto Data App",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires
)
