from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dj-app",
    version="0.1.0",
    author="DJ App Contributors",
    description="DJ Mixer aplikace pro Linux Debian s podporou MP3, WAV, YouTube a Spotify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ozvuceniblatnice/dj-app",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dj-app=dj_app.main:main",
        ],
    },
)
