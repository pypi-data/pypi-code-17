import vagrepo.cli
import vagrepo.repository

def main():
    namespace = vagrepo.cli.parse_args()
    vagrepo.cli.handle(namespace)
