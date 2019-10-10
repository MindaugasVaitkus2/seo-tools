import setuptools

setuptools.setup(
    name="seo-tools",
    version="2.0.0",
    description=open("README.md").readlines()[1][:-1],
    author="0xhtml",
    license=open("LICENSE").readlines()[0][:-1],
    packages=["seo_tools"],
    entry_points={
        "console_scripts": ["seo-tools=seo_tools.cli:main"]
    },
    install_requires=[x[:-1] for x in open("requirements.txt").readlines()]
)
