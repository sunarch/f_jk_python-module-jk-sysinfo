################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: Apache Software License",
		"Topic :: System :: Monitoring",
	],
	description = "This python module provides ways to retrieve and parse technical data of (Linux) computer systems.",
	download_url = "https://github.com/jkpubsrc/python-module-jk-sysinfo/tarball/0.2020.2.16.1",
	include_package_data = False,
	install_requires = [
		"python-dateutil",
		"fabric",
		"pytz",
		"jk_console",
	],
	keywords = [
		"monitoring",
	],
	license = "Apache 2.0",
	name = "jk_sysinfo",
	packages = [
		"jk_sysinfo",
	],
	scripts = [
		"bin/sysinfo.py",
	],
	url = "https://github.com/jkpubsrc/python-module-jk-sysinfo",
	version = "0.2020.2.16.1",
	zip_safe = False,
	long_description = readme(),
	long_description_content_type="text/markdown",
)
