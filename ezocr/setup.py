from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.readlines()

setup(
    name="easyocrlite",
    packages=find_packages(exclude=["pics"]),
    python_requires=">=3.6",
    include_package_data=True,
    version="0.0.1",
    install_requires=requirements,
    license="Apache License 2.0",
    description="",
    long_description="",
    keywords=["ocr optical character recognition deep learning neural network"],
    classifiers=["Development Status :: 5 - Production/Stable"],
)
