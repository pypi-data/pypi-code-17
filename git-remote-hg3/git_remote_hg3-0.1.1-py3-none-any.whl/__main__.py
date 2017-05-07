def main():
    import sys
    import git_remote_hg
    try:
        res = git_remote_hg.main()
    except KeyboardInterrupt:
        res = 1
    sys.exit(res)


if __name__ == "__main__":
    main()