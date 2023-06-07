from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in aimgpt/__init__.py
from aimgpt import __version__ as version

setup(
	name="aimgpt",
	version=version,
	description="AIMGPT",
	author="Xurpas Inc.",
	author_email="andy@xurpas.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
