from setuptools import setup, find_packages

setup(
    name="stage0_py_utils",
    version="0.1.5",
    description="A utility package for stage0 microservices",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    packages=find_packages(where="."),
    python_requires=">=3.8",
    install_requires=[
        "flask",
        "pymongo",
        "discord",
        "ollama"
    ],
    extras_require={
        "dev": ["black", "pytest", "unittest"]
    },
    include_package_data=True,
)