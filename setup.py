import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="analog_noise_estimator",
    version="1.0.0",
    author="Slawomir Figiel",
    author_email="fivitti@gmail.com",
    description="Estimate analog noise on the images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gut-space/analog-noise-estimator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy"],
    python_requires='>=3.6',
)