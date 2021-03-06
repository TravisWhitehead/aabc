import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aabc",
    version="1.0.0",
    author="Travis Whitehead",
    author_email="TravisWhitehead@protonmail.com",
    description="Tool that queries Google Play Store to check if apps on a device use Android App Bundles",
    entry_points={
        'console_scripts': [
            'aabc = aabc.aabc:main'
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/traviswhitehead/aabc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
