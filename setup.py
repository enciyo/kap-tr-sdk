from setuptools import setup, find_packages

setup(
    name='kap_sdk',
    version='0.1.15pypi-AgEIcHlwaS5vcmcCJDg1ZDgxZjljLTBkYjAtNDQ1Yy04Nzc4LTg0MDUzNWFmOWE2NgACKlszLCIxYmRiNjMwZC0xMWRmLTQwYzYtYWI2OS03MzkwOGRiYzZhZGMiXQAABiDgiLTIjNFLMFDveOC6jgr2PlRcxcAzsVvDxi6BlgiDCg',
    description='Kap Data Scrapping',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pyppeteer',
        "diskcache"
    ],
)
