import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maoyan-font-recognize-aruix",
    version="0.1.0",
    author="aruix",
    author_email="aruix@teaforence.com",
    description="A lib to recognize MaoYan font from the offical website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aruiplex/MaoYanFontRecognize",
    project_urls={
        "Bug Tracker": "https://github.com/aruiplex/MaoYanFontRecognize/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=["MaoYanFontRecognize"],
    python_requires=">=3.6",
    install_requires = ["beautifulSoup4", "fonttools"],
    include_package_data=True
)
