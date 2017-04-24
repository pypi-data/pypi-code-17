
import sys
import os
import logging
from jip.embed import require
from jip.maven import Artifact
from jip.cache import cache_manager
from zipfile import ZipFile
import gzip
import shutil


class Moven:

    JAR_DIRS_LAYOUT = "META-INF/resources/models/"

    def __init__(self, path="models.txt", dir="./moven"):
        if os.path.isfile(path):
            self.path = path
        else:
            raise ValueError("invalid path '%s'" % path)
        self.dir = os.path.abspath(dir)
        self.log = logging.getLogger("moven")

    def install(self):
        self.log.debug("reading dependencies from '%s'..." % self.path)

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        with open(self.path, "r") as f:
            for line in f:
                if len(line.strip()) > 0 and not line.startswith("#"):
                    dependency = line.strip()
                    if self._retrieve(dependency):
                        self._extract_models(dependency)

    def _retrieve(self, dependency):
        try:
            require(dependency)
            self.log.info("successfully installed '%s'" % dependency)
            return True
        except:
            e = sys.exc_info()[0]
            self.log.error("error retrieving '%s': %s", dependency, repr(e))
            return False

    def _extract_models(self, dependency):
        artifact = Artifact.from_id(dependency)
        jar_path = cache_manager.get_jar_path(artifact, filepath=True)
        target_dir = os.path.abspath(os.path.join(self.dir, artifact.artifact))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        self.log.debug("reading models from artifact '%s'..." % jar_path)
        with ZipFile(jar_path, "r") as zip:
            count = 0
            for name in zip.namelist():
                if name.startswith(self.JAR_DIRS_LAYOUT):
                    rel_path = name[len(self.JAR_DIRS_LAYOUT):]
                    if len(rel_path) > 0:
                        target = os.path.join(target_dir, rel_path)
                        if name.endswith('/') and not os.path.exists(self.dir):
                            os.makedirs(target)
                        else:
                            with open(target, "wb") as f:
                                f.write(zip.read(name))
                            if target.endswith(".gz"):
                                self.log.debug("uncompressing %s..." % target)
                                uncompressed_target = target[:-3]
                                with gzip.open(target, "rb") as f_in:
                                    with open(uncompressed_target, "wb") as f_out:
                                        shutil.copyfileobj(f_in, f_out)
                                os.remove(target)
                            count += 1
        self.log.info("extracted %d model files to %s", count, target_dir)


def main():
    if len(sys.argv) > 1:
        moven = Moven(sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else Moven(sys.argv[1])
        moven.install()
    else:
        print("Usage: moven models.txt")


if __name__ == "__main__":
    main()
