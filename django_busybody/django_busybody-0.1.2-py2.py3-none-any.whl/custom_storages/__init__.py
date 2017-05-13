# coding: utf-8
from .chain import ChainStorage  # NOQA
try:
    from .s3 import (  # NOQA
        StaticS3Storage, ManifestFilesStaticS3Storage,
        MediaS3Storage, HashedMediaS3Storage)
except ImportError:  # pragma: no cover
    raise
