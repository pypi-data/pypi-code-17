import os

from conan.test_package_runner import TestPackageRunner


def run():
    the_json = os.getenv("CONAN_RUNNER_ENCODED", None)
    runner = TestPackageRunner.deserialize(the_json)
    runner.run()

if __name__ == '__main__':
    run()
