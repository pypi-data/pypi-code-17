from .cli import main as cmain, runner

def main():
    runner(cmain())

if __name__ == "__main__":
    main()