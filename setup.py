from setuptools import find_packages, setup

_version = '0.0.5'
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
    license='MIT',
    include_package_data=True,
    data_files=[('boiler_templates', ['boiler_templates/dtpt-1.md'])],
    zip_safe=False,
    keywords = ['docx', 'md', 'xml'],
    install_requires=[
        'python-docx',
        'mistletoe',
        'webcolors',
        'cvss',
        'natsort',
        'docxcompose',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    scripts=["docxtool.py", "boilergen.py"],
)
