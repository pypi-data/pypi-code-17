import webbrowser
import sys,os,markdown2

def main():
    inp = sys.stdin.read()
    print inp
    filename = "output.html"
    file = open(filename,"w")
    file.write(markdown2.markdown(inp))
    file.close()
    webbrowser.open('file://' + os.path.realpath("output.html"))
    """
    sys.stdin.flush()
    save = None
    while save == None:
        save = True if input("Press enter to end. Press s and then enter, to save output as %s"%(filename)) == "" else False if "s" else None
    if not save:
        os.remove(filename)
    """
if __name__ == "__main__":
    main()