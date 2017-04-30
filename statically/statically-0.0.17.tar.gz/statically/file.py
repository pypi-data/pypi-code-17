from pathlib import Path

#Obter caminho relativo de um ficheiro para a root do server
def relative_root(file):
    aux = file
    path = Path(".")
    while not ".statically" in [a.name for a in aux.parent.iterdir()]:
        path = path.joinpath("..")
        aux = aux.parent
    #Off by one corrected
    return Path(*path.parts[:-1])

def convert_path(file):
    parts = list(file.parts)
    parts[parts.index("content")] = "public"
    parts[-1] = parts[-1].replace(".md", ".html")

    return Path(*parts)

def write(file, content):
    if not file.parent.exists():
        file.parent.mkdir(parents=True)

    file = open(file, 'w')
    file.write(content)
