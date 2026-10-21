from setuptools import setup, find_packages

setup(
    name="slm_reviewer",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "slm-reviewer=slm_reviewer.cli:main",
        ],
    },
)