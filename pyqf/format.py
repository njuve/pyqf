from typing import List
import re
import json
from pyqf.helpers import add_upper_reserved_words


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
        sum(a) over (partition by b),
        count(b)
    FROM
        t
    GROUP BY
        c
    """
    return Format(query=query).run()


class Format:
    def __init__(self, query: str):
        config = json.load(open("src/conf.json"))
        reserved_word_lower = config["reserved_word_lower"]
        self.reserved_words = add_upper_reserved_words(reserved_word_lower)
        self.query = self.to_uppercase(
            [
                val for val in re.split("(" + "|".join(self.reserved_words + [".*,"]) + ")", query) if val != ""
            ]  # str query to list splited by reserved words
        )

    def to_uppercase(self, query):
        def reservedword2uppercase(word):
            if word in self.reserved_words:
                result_word = word.upper().strip()
            else:
                result_word = word.strip()

            return result_word

        return [reservedword2uppercase(word) for word in query]

    def indent(self, query: List[str]) -> List[str]:
        def insert_indent(word):
            count_reserved_word = sum([1 for reversed_word in self.reserved_words if reversed_word in word])
            if count_reserved_word > 0:
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
