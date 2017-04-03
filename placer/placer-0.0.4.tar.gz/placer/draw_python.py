WHITE = "0"
BLACK = "3"
GREY = "1"
YELLOW = "8"
# 9
# A
# B
# C
BLUE = "D"

translate_int = {color: num for num, color in enumerate("0123456789ABCDEF")}
translate_color = {
    "0": "white",
    "1": "grey",
    "3": "black",
    "8": "yellow",
    "D": "blue"
}


def html_template(j, color):
    offset = "left: " + str(50 * j) + "px;" if j else ""
    style = "height: 49px; width: 49px; position: absolute; {}"
    style += "background-color: {};"
    style = style.format(offset, color)
    style += "border: 1px solid black; "
    return '<span style="{}"></span>'.format(style)


def htmlize(frmt):
    inner = "<br>".join(["".join([html_template(j, translate_color[y]) for j, y in enumerate(x)])
                         for i, x in enumerate(python_format)])
    return "<html><body>{}</body></html>".format(inner)

python_format = [
    GREY * 26,
    GREY * 9 + BLUE * 8 + GREY * 9,
    GREY * 8 + BLUE * 2 + WHITE + BLUE * 7 + GREY * 8,
    GREY * 8 + BLUE * 10 + GREY * 8,
    GREY * 8 + BLUE * 10 + GREY * 8,
    GREY * 14 + BLUE * 4 + YELLOW * 4 + GREY * 4,
    GREY * 6 + BLUE * 12 + YELLOW * 5 + GREY * 3,
    GREY * 5 + BLUE * 13 + YELLOW * 5 + GREY * 3,
    GREY * 5 + BLUE * 13 + YELLOW * 5 + GREY * 3,
    GREY * 5 + BLUE * 13 + YELLOW * 5 + GREY * 3,
    GREY * 5 + BLUE * 5 + YELLOW * 13 + GREY * 3,
    GREY * 5 + BLUE * 5 + YELLOW * 13 + GREY * 3,
    GREY * 5 + BLUE * 5 + YELLOW * 13 + GREY * 3,
    GREY * 5 + BLUE * 5 + YELLOW * 12 + GREY * 4,
    GREY * 6 + BLUE * 4 + YELLOW * 4 + GREY * 12,
    GREY * 10 + YELLOW * 10 + GREY * 6,
    GREY * 10 + YELLOW * 10 + GREY * 6,
    GREY * 10 + YELLOW * 7 + WHITE + YELLOW * 2 + GREY * 6,
    GREY * 11 + YELLOW * 8 + GREY * 7,
    GREY * 26,
    GREY * 26,
    #
    GREY * 1 + BLACK * 3 + GREY + BLACK + GREY + BLACK + GREY + BLACK * 3 + GREY +
    BLACK + GREY + BLACK + GREY + BLACK * 3 + GREY + BLACK + GREY * 2 + BLACK + GREY,
    #
    GREY * 1 + BLACK + GREY + BLACK + GREY + BLACK + GREY + BLACK + GREY * 2 + BLACK + GREY * 2 +
    BLACK + GREY + BLACK + GREY + BLACK + GREY + BLACK + GREY + BLACK * 2 + GREY + BLACK + GREY,
    #
    GREY * 1 + BLACK * 3 + GREY * 2 + BLACK + GREY * 3 + BLACK + GREY * 2 + BLACK *
    3 + GREY + BLACK + GREY + BLACK + GREY + BLACK + GREY + BLACK * 2 + GREY,
    #
    GREY * 1 + BLACK + GREY * 4 + BLACK + GREY * 3 + BLACK + GREY * 2 + BLACK +
    GREY + BLACK + GREY + BLACK * 3 + GREY + BLACK + GREY * 2 + BLACK + GREY,
    #
    GREY * 26
]


python_logo = []
for x in range(26):
    for y in range(26):
        color = translate_int[python_format[y][x]]
        python_logo.append({"x": x, "y": y, "color": color})

python_html = htmlize(python_format)
