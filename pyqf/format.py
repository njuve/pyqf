from typing import List
import re
import json
from pyqf.helpers import add_uppercases


def format(query: str) -> str:
    """query formater

    Parameters
    ----------
    query : str

    Returns
    -------
    str
        formated query

    Examples
    --------
    >>> print(format("select a, b from t"))
    SELECT
        a,
        b
    FROM
        t

    >>> print(format("select sum(a) over (partition by b), count(b) from t group by c"))
    SELECT
        SUM(a) OVER (PARTITION BY b),
        COUNT(b)
    FROM
        t
    GROUP BY
        c
    """
    return Format(query=query).run()


class Format:
    def __init__(self, query: str):
        config = json.load(open("pyqf/conf.json"))
        indent_words = config["indent_words"]
        self.indent_words = add_uppercases(indent_words)
        self.only_uppercase_words = config["only_uppercase_words"]
        self.query = [
            val.strip()
            for val in re.split("(" + "|".join(self.indent_words + [".*,"]) + ")", self.to_uppercase(query))
            if val != ""
        ]  # str query to list splited by reserved words

    def to_uppercase(self, query):
        uppercases = {word: word.upper() for word in self.only_uppercase_words + self.indent_words}
        for k, v in uppercases.items():
            query = query.replace(k, v)

        return query

    def indent(self, query: List[str]) -> List[str]:
        def insert_indent(word):
            count_indent_word = sum([1 for indent_word in self.indent_words if indent_word == word])
            if count_indent_word > 0:
                indented_word = word
            else:
                indented_word = "\u0020\u0020\u0020\u0020" + word

            return indented_word

        return [insert_indent(word) for word in query]

    def break_line(self, query: List[str]) -> List[str]:
        return "\n".join(query)

    def run(self) -> str:
        indented_query = self.indent(query=self.query)
        formated_query = self.break_line(query=indented_query)

        return "".join(formated_query)
