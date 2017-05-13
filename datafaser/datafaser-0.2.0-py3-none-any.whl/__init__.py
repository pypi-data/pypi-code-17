import os
import sys
import datafaser.start


def run(files):
    try:
        datafaser.start.create_runner_to_load(files).load_and_run_all_plans()
    except Exception as e:
        sys.stderr.write('Datafaser run failed on %s: %s\n' % (e.__class__.__name__, str(e)))
        if 'datafaser_debug' in os.environ:
            raise e


