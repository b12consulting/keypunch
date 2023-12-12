from setuptools import setup


setup(
    name="keypunch",
    description="keypunch",
    version="0.0",
    url="",
    author="Bertrand Chenal",
    packages=["keypunch"],
    install_requires=["requests"],
    extras_require={
        "test": ["pytest"],
    },
)
