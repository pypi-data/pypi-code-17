import os
from pathlib import Path
from statically.md import *
from statically.render import *
from statically.file import *
from statically.settings import *


def update(path, url):
    if not os.path.exists(os.path.join(path, '.statically')):
        print(f"Error: {path} is not a statically instance")
        exit()
    pages = {}
    #read generic settings for website
    settings = read_settings(path / Path("config.yml"))

    #iterate over all the files and generate a html, config tuple indexed by
    #the path in a dictionary
    for file in (path / Path("content")).rglob('*.md'):
        print("Converting", file)
        with file.open() as f:
            content = f.read()
            #convert to markdown, get the file specific configs
            compiled, page_settings = compile(content, settings)

        pages[convert_path(file)] = (compiled, page_settings)

    #crate jinja environment with template folder
    jinja_env = make_env(path / Path('template'))
    jinja_env.globals.update(zip=zip)

    #iterate over the pages and let jinja render them
    for file, page in pages.items():
        print("Writing", file)
        compiled, page_settings = page
        #jinja templates api
        render_params = build_jinja_api(page_settings, file, list(pages.keys()), compiled)
        rendered = render(jinja_env, render_params)

        write(Path(file), rendered)

