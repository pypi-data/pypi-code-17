

help_topic = 'Table operation'
help_text = '''
Convert table data (from CSV files) to objects with named fields:

    - "Convert a table":
        - table:
          from:
            branch: "csv-data"
            table:
              headers:
                - rows: 1
          to:
            branch: "objects from spreadsheet"

First row of table at from.branch is used as field names.
Each subsequent row is converted into an object with values named by those field names:

    csv-data:
      - [ "first fieldname", "second fieldname" ]
      - [ "value 1 on row 1", "value 2 on row 1" ] 
      - [ "value 1 on row 2", "value 2 on row 2" ]

    objects from spreadsheet:
      - first fieldname: value 1 on row 1
        second fieldname: value 2 on row 1
      - first fieldname: value 1 on row 2
        second fieldname: value 2 on row 2
'''


def convert(data_tree, directives):
    from_branch = directives['from']['table']['branch']
    to_branch = directives['to']['branch']

    source = data_tree.reach(from_branch)
    headers = source[0]
    target = []
    for row in source[1:]:
        o = {}
        for i in range(0, len(headers)):
            o[headers[i]] = row[i]
        target.append(o)
    data_tree.merge(target, to_branch)
