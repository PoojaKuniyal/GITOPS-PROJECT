from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ARGOCD_SMART",
    version="0.1",
    author="Pooja",
    packages=find_packages(),
    install_requires = requirements,
)