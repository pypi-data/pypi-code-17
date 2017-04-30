import jinja2
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from statically.file import relative_root

def make_env(path):
    return Environment(loader=FileSystemLoader(str(path)))

def render(jinja_env, render_params):

    template = jinja_env.get_template(render_params["template"]+".html")
    return template.render(**render_params)

#generate the api acessable by the jinja templates
def build_jinja_api(config, path, filenames, content):
    relative_path = relative_root(path)
    for  resource in ["style", "colorscheme"]:
        config[resource] = relative_path / Path(resource) / Path(config[resource])
        config[resource] = str(config[resource]) + ".css"
  
    #list of filenames
    names = [name.stem for name in filenames]

    return {**config, **{"content": content}, **{"files": filenames},
           "filenames": names}

