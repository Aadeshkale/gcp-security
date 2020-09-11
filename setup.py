import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gcpsecurity",
    version="0.0.3",
    author="Aadesh Kale",
    author_email="aadeshkale619@gmail.com",
    description="Small package used to analyze or improve gcp security of GCP cloud resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aadeshkale/gcp-security",
    packages=setuptools.find_packages(),
    install_requires=["google-api-python-client >= 1.11.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)