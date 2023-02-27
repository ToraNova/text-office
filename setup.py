from setuptools import find_packages, setup

_version = '0.0.7'
_packages = find_packages()

setup(
    name='document-reporter',
    version=_version,
    description='a python module to create reports from text-based files (e.g., markdown, xml)',
    packages=_packages,
    author='Chia Jason',
    author_email='chia_jason96@live.com',
    url='https://github.com/toranova/document-reporter/',
    download_url='https://github.com/ToraNova/document-reporter/archive/refs/tags/v%s.tar.gz' % _version,
    license='AGPL-3.0-or-later',
    include_package_data=True,
    data_files=[('boiler_templates', ['boiler_templates/dtpt-1.md', 'boiler_templates/images.md'])],
    zip_safe=False,
    keywords = ['docx', 'md', 'xml'],
    install_requires=[
        'cvss==2.5',
        'docxcompose==1.3.4',
        'lxml==4.8.0',
        'mistletoe==0.8.2',
        'natsort==8.1.0',
        'python-docx==0.8.11',
        'six==1.16.0',
        'webcolors==1.11.1',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    scripts=["docxtool.py", "boilergen.py"],
)
