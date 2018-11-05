import setuptools
import pathlib


here = pathlib.Path(__file__).absolute().parent
readme = (here / "README.md").read_text()
about = {}

exec((here / "mailmitt" / "__version__.py").read_text(), about)

setuptools.setup(
    name="mailmitt",
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    author="Trevor Morgan",
    packages=["mailmitt"],
    url="https://github.com/trvrm/mailmitt",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.5",
    install_requires=["aiohttp", "aiosmtpd", "bottle"],
    entry_points={"console_scripts": ["mailmitt = mailmitt.__main__:main"]},
    package_data={"mailmitt": ["static/*", "templates/*"]},
)
