from setuptools import setup

setup(
    name="pymporter",
    version="0.1.0",
    description="Dynamic requirements loader for Python projects.",
    long_description="Lightweight module to install and import runtime requirements from a requirements.txt file.",
    long_description_content_type="text/plain",
    author="Ander Emiliano Santos Ponce",
    author_email="anderemilianosantosponce@local",
    url="https://github.com/AnderSantos113/pymporter",
    py_modules=["importer"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
