from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hallucinationbench",
    version="0.1.0",
    author="Devasish Banerjee",
    author_email="bdeva1975@gmail.com",
    description="Detect hallucinations in your RAG pipeline output in two lines of Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bdeva1975/hallucinationbench",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "httpx>=0.27.0",
    ],
)