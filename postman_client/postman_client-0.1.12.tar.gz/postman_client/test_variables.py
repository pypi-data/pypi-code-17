variables = {
    "recipients": [
        "Thiago de Castro <thiago.decastro2@gmail.com>",
        "Thiago C de Castro <THIAGO.CIRRUS@ALTERDATA.COM.BR>",
        "<success@simulator.amazonses.com>",
        "<bounce@simulator.amazonses.com>",
        "<ooto@simulator.amazonses.com>",
        "<complaint@simulator.amazonses.com>",
        "<suppressionlist@simulator.amazonses.com>",
    ],
    "context_per_recipient": {
        "thiago.decastro2@gmail.com": {"foo": True},
        "thiago.cirrus@alterdata.com.br": {"bar": True}
    },
    "from_name": 'Postman',
    "from_email": 'postman@alterdata.com.br',
    "template_name": 'test-101',
    "message_text": "Using this message instead.",
    "message_html": "<em>Using this message <strong>instead</strong>.</em>",
    "key": '1e4be7cdd03545958e34',
    "secret": 'cf8cdba282104ed88f0a'
}
server_uri_test = 'http://172.16.72.31:8000'
