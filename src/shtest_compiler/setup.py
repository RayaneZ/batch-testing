
from setuptools import setup, find_packages

setup(
    name="shtest-compiler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "compile_expr=compile_expr:main",
        ],
    },
    python_requires=">=3.8",
)
