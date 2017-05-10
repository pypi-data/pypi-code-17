from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
  dep_packages = f.readlines()
  dep_packages = [x.strip() for x in dep_packages]

setup(
    name="projectowl",
    version="0.3.3",
    description="high level computer vision library",
    keywords="computer vision image feature pipeline",
    url="https://github.com/flyfj/owl",
    author="Jie Feng",
    author_email="jiefengdev@gmail.com",
    license="MIT",
    packages=find_packages("./"),
    install_requires=dep_packages,
    include_package_data=True,
    zip_safe=False)
