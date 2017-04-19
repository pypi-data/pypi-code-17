import gzip
import os
import logging
import dill

from time import time
from bgcache.utils import md5_file, bgcache_home, md5_code

# Ignore the cache (don't load and also don't dump anything)
SKIP = "skip"


def bgcache(suffix=None, time_threshold=5):

    def decorator(old_function):
        def new_function(*args, **kwargs):

            if len(args) > 1 or len(kwargs) > 1 or (len(kwargs) == 1 and 'bgcache' not in kwargs):
                logging.error("@bgcache needs a single argument, and it must be a file path.")
                return old_function(*args, **kwargs)

            input_file = args[0]
            if not os.path.isfile(input_file):
                logging.error("@bgcache '{}' must be a valid file path.".format(input_file))
                return old_function(*args, **kwargs)

            bgcache_command = kwargs.get('bgcache', None)

            cache_suffix = str(old_function.__name__)
            if suffix is not None and not callable(suffix):
                cache_suffix = "{}_{}".format(cache_suffix, suffix)

            if bgcache_command == SKIP:
                logging.debug("@bgcache skip cache '{}'".format(cache_suffix))
                return old_function(input_file)

            file_path = os.path.abspath(input_file)
            source_md5 = md5_code(old_function)

            cache_key = os.path.join(
                bgcache_home(),
                os.path.dirname(file_path).lstrip(os.sep),
                "{}#{}#{}.bgcache".format(
                    os.path.basename(file_path),
                    cache_suffix,
                    source_md5
                )
            )

            logging.debug("@bgcache input path: {}".format(file_path))
            logging.debug("@bgcache source md5: {}".format(source_md5))
            logging.debug("@bgcache key: {}".format(cache_key))

            md5_input = None
            if os.path.exists(cache_key) and os.path.isfile(cache_key):

                # Compute file md5
                md5_input, dt = md5_file(file_path)
                logging.debug("@bgcache input md5: {} ({:.2f}s)".format(md5_input, dt))

                try:
                    with gzip.open(cache_key, 'rb') as fd:
                        md5_cache, cached_value = dill.load(fd)
                except OSError:
                    md5_cache, cached_value = None, None

                if md5_cache != md5_input:
                    logging.warning("Invalidating bgcache '{}'".format(cache_key))
                    os.unlink(cache_key)
                    cached_value = None
                else:
                    logging.debug("@bgcache Using '{}' from {}".format(cache_suffix, cache_key))
            else:
                cached_value = None

            if cached_value is not None:
                return cached_value
            else:
                logging.debug("@bgcache key not found")
                t_ini = time()
                cached_value = old_function(input_file)
                if (time() - t_ini) > time_threshold:
                    try:
                        if md5_input is None:
                            md5_input, dt = md5_file(file_path)
                            logging.debug("@bgcache input md5: {} ({:.2f}s)".format(md5_input, dt))

                        # Create folders
                        os.makedirs(os.path.dirname(cache_key), exist_ok=True)

                        # Dump the result
                        if not os.path.exists(cache_key):
                            with os.fdopen(os.open(cache_key, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o0700), 'wb') as fd:
                                with gzip.open(fd, 'wb') as fdgz:
                                    dill.dump((md5_input, cached_value), fdgz)

                    except Exception as e:
                        logging.error("@bgcache problems dumping the cache: {}".format(e))
                else:
                    logging.debug("@bgcache not caching due to time below threshold")

                return cached_value

        return new_function

    # If it's called without parentesis
    if callable(suffix):
        return decorator(suffix)

    return decorator
