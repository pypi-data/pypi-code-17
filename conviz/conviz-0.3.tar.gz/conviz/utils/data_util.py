import os
from urllib.request import urlretrieve


class DataUtil(object):
    """
    A utility class which provides data-related functionality.
    """

    @staticmethod
    def get_cache_path():
        """
        Gets the path to the cache directory of Conviz.
        
        :return: The path to the cache directory of Conviz.
        """
        return os.path.expanduser(os.path.join("~", ".conviz"))

    @staticmethod
    def load_file(file_path, origin):
        """
        Loads a file from cache, if present, otherwise downloads and caches it.
        
        :param file_path: The path to which the downloaded file will be cached.
        :param origin: The origin from which data is downloaded if not cached.
        
        :return: file_path
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            DataUtil.download_file(file_path, origin)
        return file_path

    @staticmethod
    def download_file(file_path, origin):
        """
        Downloads a file from the given origin to the given file path.
        
        :param file_path: The path to which the downloaded content is saved.
        :param origin: The origin from which the content is downloaded.
        
        :return: file_path
        """
        try:
            urlretrieve(origin, file_path)
            return file_path
        except (Exception, KeyboardInterrupt):
            if os.path.exists(file_path):
                os.remove(file_path)
            raise
