# coding: utf-8
from django.conf import settings

try:
    from storages.backends.s3boto import S3BotoStorage
    from django.contrib.staticfiles.storage import ManifestFilesMixin

    from .hashed import HashedStorageMixin
    from .overwrite import OverwriteStorageMixin

    class StaticS3Storage(S3BotoStorage):
        location = getattr(settings, 'STATICFILES_LOCATION',
                           '{}/{}'.format(getattr(settings, 'PROJECT_NAME', 'django'), 'static'))

    class ManifestFilesStaticS3Storage(ManifestFilesMixin, S3BotoStorage):
        location = getattr(settings, 'STATICFILES_LOCATION',
                           '{}/{}'.format(getattr(settings, 'PROJECT_NAME', 'django'), 'static'))

    class MediaS3Storage(S3BotoStorage):
        location = getattr(settings, 'MEDIAFILES_LOCATION',
                           '{}/{}'.format(getattr(settings, 'PROJECT_NAME', 'django'), 'media'))

    class HashedMediaS3Storage(HashedStorageMixin, OverwriteStorageMixin, MediaS3Storage):
        IGNORE_OVERWRITE = True

except ImportError:  # pragma: no cover
    pass
