import os.path

__all__ = ['PRD_VERSION', 'DATA_ROOT', 'PRD_DATA_ROOT']

DATA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
PRD_VERSION = 'PRDOPSSOC-F-008'  # updated 2017-04-26
PRD_DATA_ROOT = os.path.join(DATA_ROOT, PRD_VERSION)
