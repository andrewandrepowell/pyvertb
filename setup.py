import setuptools
import pathlib


def get_version(version_file):
    locls = {}
    exec(open(version_file).read(), {}, locls)
    return locls["__version__"]


here = pathlib.Path(__file__).parent.resolve()
readme_file = here / "README.md"
version_file = here / "src" / "pyvert" / "version.py"

setuptools.setup(
    name="pyvert",
    version=get_version(version_file),
    author="Kaleb Barrett",
    author_email="dev.ktbarrett@gmail.com",
    description="Verification framework for cocotb",
    long_description=readme_file.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/ktbarrett/pyvert",
    project_urls={
        "Bug Tracker": "https://github.com/ktbarrett/pyvert/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["cocotb>=1.5"],
)
