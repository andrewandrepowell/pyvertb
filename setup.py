from typing import Union
import setuptools
import pathlib
import os


def get_version(
    version_file: Union[str, os.PathLike], version_var: str = "__version__"
):
    locls = {}
    exec(open(version_file).read(), {}, locls)
    return locls[version_var]


here = pathlib.Path(__file__).parent.resolve()
readme_file = here / "README.md"
version_file = here / "src" / "pyvertb" / "version.py"

setuptools.setup(
    name="pyvertb",
    version=get_version(version_file),
    author="Kaleb Barrett",
    author_email="dev.ktbarrett@gmail.com",
    description="Verification framework for cocotb",
    long_description=readme_file.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/ktbarrett/pyvertb",
    project_urls={
        "Bug Tracker": "https://github.com/ktbarrett/pyvertb/issues",
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
