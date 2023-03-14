from setuptools import find_packages, setup

from text_office import version
_packages = find_packages()

setup(
    name='text-office',
    version=version,
    description='a python module to create office documents from text-based files (e.g., markdown, xml)',
    packages=_packages,
    author='Chia Jason',
    author_email='chia_jason96@live.com',
    url='https://github.com/toranova/text-office/',
    download_url='https://github.com/ToraNova/text-office/archive/refs/tags/v%s.tar.gz' % version,
    license='AGPL-3.0-or-later',
    include_package_data=True,
    data_files=[('boiler_templates', ['boiler_templates/dtpt-1.md'])],
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
    scripts=["text-office.py", "boilergen.py"],
)
