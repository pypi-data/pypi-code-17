"""
The test environment exists during test runtime
"""


class Environment(object):
    """
    Test environment instance
    """
    from typing import List, Dict

    def __init__(self, config: Dict, test_paths: List[str]):
        self.config = config
        self.test_paths = test_paths
