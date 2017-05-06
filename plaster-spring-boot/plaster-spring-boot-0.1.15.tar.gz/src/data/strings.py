import types as types


class Docs:
    version = 'fetches the current version of the tool'

    generation_mode = 'whether to generate or delete\n' \
                      '    generate, g - create files\n' \
                      '    delete, d - remove files'

    generation_mode_choices = [
        'generate',
        'g',
        'delete',
        'd'
    ]

    generation_type = 'how to generate or delete content\n' \
                      '    scaffold - all files associated to the model\n' \
                      '    model - the entire model\n' \
                      '    repository - the entire repository\n' \
                      '    service - the entire service\n' \
                      '    controller - the entire controller\n' \
                      '    field - individual field(s)'

    generation_type_choices = [
        'scaffold',
    ]
    generation_type_choices += types.ALL

    model = 'name of model for which to perform actions'

    fields = 'fields to perform actions listed as name:type pairs'

    key = 'indicates the following field:type pair should define the key\n' \
          'NOTE: should be a trailing param'

    dir = 'defines a sub path in which to perform actions\n' \
          'NOTE: should be a trailing param'
