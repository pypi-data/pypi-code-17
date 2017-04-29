import os
import sys
import logging
import logging.config

# Let submodules use full name even when run without installing
base_dir = os.path.dirname(os.path.dirname(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)


if __name__ == '__main__':
    from datafaser.main import main
    main(sys.argv)
