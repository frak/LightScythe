import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="light-scythe-frak",
    version="0.0.1",
    author="Michael Davey",
    author_email="m.davey.bsc@gmail.com",
    description="A Raspberry Pi Light Scythe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frak/LightScythe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'scythe = scythe.Scythe:run',
            'scy-reset = scythe.reset:clear',
        ],
    },
)
