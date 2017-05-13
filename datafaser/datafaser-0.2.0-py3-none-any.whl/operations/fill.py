from jinja2 import Template


help_topic = 'Fill operation'
help_text = '''
Fill in a template with current values.

    - "Generate file contents":
        - fill:
            from:
                branch: "context"
            to:
                branch: "filled"
            template: "my_template_file_contents"

See http://jinja.pocoo.org/
'''


def convert(data_tree, directives):
    from_branch = directives['from']['branch']
    to_branch = directives['to']['branch']
    template_branch = directives['template']

    source = data_tree.reach(from_branch)
    template_content =  data_tree.reach(template_branch)
    filled = Template(template_content).render(source)

    data_tree.merge(filled, to_branch)
