import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


PROJECT_NAME = "image_scrapper"
USER_NAME = "pk1308"
SRC_REPO = ""

setuptools.setup(
    name=f"{PROJECT_NAME}-{USER_NAME}",
    version="0.0.7",
    author=USER_NAME,
    author_email="princevkurien@gmail.com",
    description="Image scrapping from google",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NAME}/{PROJECT_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{USER_NAME}/{PROJECT_NAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.1",
    install_requires=[
        "selenium",
    "webdriver_manager"  ]
)