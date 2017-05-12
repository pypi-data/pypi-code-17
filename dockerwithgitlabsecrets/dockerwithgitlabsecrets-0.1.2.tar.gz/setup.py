from setuptools import setup, find_packages

try:
    from pypandoc import convert
    def read_markdown(file: str) -> str:
        return convert(file, "rst")
except ImportError:
    def read_markdown(file: str) -> str:
        return open(file, "r").read()

setup(
    name="dockerwithgitlabsecrets",
    author="Colin Nolan",
    author_email="colin.nolan@sanger.ac.uk",
    version="0.1.2",
    packages=find_packages(exclude=["tests"]),
    install_requires=open("requirements.txt", "r").readlines(),
    url="https://github.com/wtsi-hgi/docker-with-gitlab-secrets",
    license="MIT",
    description="Wraps Docker to run with GitLab build variables",
    long_description=read_markdown("README.md"),
    entry_points={
        "console_scripts": [
            "docker-with-gitlab-secrets=dockerwithgitlabsecrets.entrypoint:main",
        ]
    }
)
