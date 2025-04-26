from setuptools import setup, find_packages

setup(
    name='kap_sdk',
    version='0.1.15',
    description='Kap Data Scrapping',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pyppeteer',
        "diskcache"
    ],
)
