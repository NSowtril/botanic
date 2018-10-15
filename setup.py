# 描述项目以及从属的文件
from setuptools import find_packages, setup

setup(
    name='botanic_website',
    version='1.0.0',
    packages=find_packages(),  
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)