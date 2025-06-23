from setuptools import setup

setup(
    name="py2ccompiler",
    version="1.0",
    py_modules=["cli", "compiler"],
    entry_points={
        "console_scripts": ["py2c=cli:main"]
    },
)
