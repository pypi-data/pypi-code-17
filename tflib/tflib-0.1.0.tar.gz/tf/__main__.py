if __name__ == "__main__":
    import sys
    from os import environ

    import yaml

    from tf.environment import Environment

    # Load config
    with open(environ.get("TFCONFIG", "tf.yml")) as f:
        config = yaml.load(f)

    # Initialize environment
    e = Environment(
        config=config,
        test_paths=sys.argv[1:]
    )
