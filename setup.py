import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reinit",
    version="0.0.2",
    author="Shresth Dewan",
    author_email="shresthdewan@gmail.com",
    description="To re-initialize and push any github repository to your own github.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zapp-oz/AutoGit",
    packages=['reinit'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pygit2==1.3.0', 'requests == 2.24.0'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts':[
            'reinit=reinit.app:main'
        ]
    }
)