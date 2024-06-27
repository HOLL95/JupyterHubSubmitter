from setuptools import setup, find_packages

setup(
    name="JupyterHubSubmitter",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        "GitPython",
    ],
    python_requires='>=3.6',
)