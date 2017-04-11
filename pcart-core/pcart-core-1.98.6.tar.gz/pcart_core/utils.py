
def get_settings_upload_path(site_id, filename):
    import os
    path = os.path.join(
        'theme-config',
        'site-%s' % site_id,
    )
    if filename is not None:
        path = os.path.join(path, filename)
    return path


def get_settings_upload_url(site_id, filename):
    from django.core.files.storage import default_storage
    path = get_settings_upload_path(site_id, filename)
    return default_storage.url(path)


def slugify_unicode(value):
    import slugify
    result = slugify.slugify(value, only_ascii=True)
    return result
