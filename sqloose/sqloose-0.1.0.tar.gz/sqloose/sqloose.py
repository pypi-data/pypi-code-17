# -*- coding: utf-8 -*-

"""
This module implements sqloose, a SQL-like query language that maps to SQL. sqloose is
not a database itself, but instead translates from sqloose to SQL.

sqloose is designed as a less rigid SQL, offering a more convenient syntax. In
particular, it allows ranges and negative indexes to be used in GROUP BY and ORDER BY
statements. The right index in the range specifies the final item. This is unlike Python
where the right index is the final item + 1.

Take the following SQL statement:

SELECT age, race, gender, count(*) AS num FROM stats GROUP BY 1,2,3 ORDER BY 4 DESC

In sqloose this can be represented many ways, such as:

SELECT age, race, gender, count(*) AS num FROM stats GROUP BY [1:3] ORDER BY -1 DESC
SELECT age, race, gender, count(*) AS num FROM stats GROUP BY [:3] ORDER BY -1 DESC
SELECT age, race, gender, count(*) AS num FROM stats GROUP BY [:-2] ORDER BY -1 DESC

Further, sqloose defines the GROUP TO and GROUP THROUGH constructs, which can be used in
the same scenario:

SELECT age, race, gender, count(*) AS num FROM stats GROUP TO -1 ORDER BY -1 DESC
SELECT age, race, gender, count(*) AS num FROM stats GROUP TO 4 ORDER BY -1 DESC
SELECT age, race, gender, count(*) AS num FROM stats GROUP THROUGH 3 ORDER BY -1 DESC
"""
import sqlparse
import sqlparse.keywords

__version__ = '0.1.0'

# There's a voice in my head that thinks this is a really bad idea.
sqlparse.keywords.KEYWORDS['THROUGH'] = sqlparse.tokens.Keyword

class Situation(object):
    """We extend GROUP BY to also permit GROUP TO and GROUP THROUGH."""
    by = 1
    to = 2
    through = 3

def is_number(value):
    """Return if value is numeric, based on attempting to coerce to float.

    :param value: The value in question.
    :returns: True if the float(value) does not throw an exception, otherwise False.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def string_to_index(needle, columns):
    """Given a string, find which column index it corresponds to.

    :param needle: The string to look for.
    :param columns: The list of columns to search in.
    :returns: The index containing that string.
    :raises ValueError: Value "`needle`" not found in columns "`columns`"
    """
    for index, value in enumerate(columns):
        if needle == value:
            return index + 1

    raise ValueError("Value \"{0}\" not found in columns \"{1}\"".format(needle, columns))

def number_to_index(value, num_columns):
    """Given a number and a number of columns, convert the number to an absolute index.

    :param value: The raw index (could be negative).
    :param num_columns: The maximum number of columns available.
    :returns: The adjusted positive column number.
    :raises ValueError: Only `num_columns` columns present, cannot index "`value`"
    """
    if abs(value) > num_columns:
        raise ValueError("Only {0} columns present, cannot index \"{1}\"".format(num_columns,
                                                                                 value))
    elif value > 0:
        return value

    return num_columns + value + 1

def _parse_bracket_range(token, columns, situation):
    """Given a Python-style range, translate it to a full range.

    :param token: The full token (e.g. "[1:3]").
    :param columns: The list of columns available.
    :param situation: A `Situation` indicating GROUP BY, GROUP THROUGH, or GROUP TO.
    :returns: A string of comma-separated columns.
    :raises ValueError: Only "by" supports bracket indexing.
    :raises ValueError: Right index greater than left index.
    """
    if situation != Situation.by:
        raise ValueError("Only \"by\" supports bracket indexing")

    num_columns = len(columns)

    if ":" not in token.value:
        item = token.value[1:-1]
        if is_number(item):
            return str(number_to_index(int(item), num_columns))

        # Note that it doesn't make much sense for a user to do this
        return item

    left = token.value[1:token.value.find(":")]
    right = token.value[token.value.find(":") + 1:-1]

    if not left:
        left = 1

    if not right:
        right = -1

    if is_number(left):
        left_index = number_to_index(int(left), num_columns)
    else:
        left_index = string_to_index(left, columns)

    if is_number(right):
        right_index = number_to_index(int(right), num_columns)
    else:
        right_index = string_to_index(right, columns)

    if left_index > right_index:
        raise ValueError("Right index greater than left index")

    return ",".join(map(str, range(left_index, right_index + 1)))

def _translate_index(token, columns, situation):
    """Translate a token to SQL columns.

    :param token: The full token (e.g. "[1:3]").
    :param columns: The list of columns available.
    :param situation: A `Situation` indicating GROUP BY, GROUP THROUGH, or GROUP TO.
    :returns: A string of comma-separated columns.
    :raises ValueError: Unmatched brackets.
    :raises ValueError: Cannot GROUP TO the first index.
    """
    # Handle the case where ASCENDING or DESCENDING are used.
    if token.is_group():
        return "".join([_translate_index(x, columns, situation) for x in token.tokens])

    if (token.value.startswith("[") != token.value.endswith("]")
            or token.value == "[" or token.value == "]"):
        raise ValueError("Unmatched brackets")

    if (token.is_whitespace() or
            token.ttype in (sqlparse.tokens.Punctuation, sqlparse.tokens.Keyword.Order)):
        return token.value

    if token.value.startswith("["):
        return _parse_bracket_range(token, columns, situation)

    if is_number(token.value):
        index = number_to_index(int(token.value), len(columns))

        if situation == Situation.by:
            return str(index)
        elif situation == Situation.to:
            if index == 1:
                raise ValueError("Cannot GROUP TO the first index")
            return ",".join(map(str, range(1, index)))
        elif situation == Situation.through:
            return ",".join(map(str, range(1, index + 1)))

    return token.value

def _get_columns(statement):
    """Get the available columns in the query `statement`.

    :param statement: A SQL SELECT statement.
    :returns: A list of columns that are being selected.
    """
    expecting_columns = False
    for token in statement.tokens:
        if token.is_whitespace():
            pass
        elif token.ttype is sqlparse.tokens.DML and token.value.upper() == "SELECT":
            expecting_columns = True
        elif expecting_columns:
            return [x.value for x in token.flatten() if x.ttype is sqlparse.tokens.Name]

def _statement_to_sql(statement):
    """Translate a sqloose statement to SQL.

    :param statement: A single statement in sqloose format.
    :returns: A string containing the corresponding SQL.
    :raises ValueError: Only group types are BY, TO, and THROUGH
    :raises ValueError: Unmatched brackets.
    """
    result = ''

    expecting_index_type = False
    expecting_group_items = False
    group_type = None
    situation = Situation.by

    for token in statement.tokens:
        if token.is_whitespace():
            result += token.value
        elif expecting_group_items:
            expecting_group_items = False
            columns = _get_columns(token.parent)
            if token.is_group():
                for item in token:
                    result += _translate_index(item, columns, situation)
            else:
                result += _translate_index(token, columns, situation)
        elif token.is_group():
            result += _statement_to_sql(token)
        elif token.value == "]":
            raise ValueError("Unmatched brackets")
        elif token.ttype is sqlparse.tokens.Keyword and token.value.upper() in ["GROUP", "ORDER"]:
            expecting_index_type = True
            result += token.value
        elif expecting_index_type:
            expecting_group_items = True
            expecting_index_type = False
            group_type = token.value.upper()
            if group_type == 'BY':
                situation = Situation.by
            elif group_type == 'TO':
                situation = Situation.to
            elif group_type == 'THROUGH':
                situation = Situation.through
            else:
                raise ValueError("Only group types are BY, TO, and THROUGH")

            if token.value.islower():
                result += 'by'
            else:
                result += 'BY'
        else:
            result += token.value

    return result

def statement_to_sql(statement):
    """Translate a sqloose statement to SQL, confirming its type first.

    :param statement: A single statement in sqloose format.
    :returns: A string containing the corresponding SQL.
    :raises TypeError: Needs to be a sqlparse.sql.Statement type
    """
    if not isinstance(statement, sqlparse.sql.Statement):
        raise TypeError("Needs to be a sqlparse.sql.Statement type")

    return _statement_to_sql(statement)

def to_sql(query):
    """Take a sqloose query and translate it to SQL.

    :param query: A sqloose query.
    :returns: An equivalent SQL query.
    """
    result = ''
    for statement in sqlparse.parse(query):
        result += statement_to_sql(statement)
    return result

if __name__ == "__main__":
    pass
