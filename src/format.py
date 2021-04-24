from typing import List
import re


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

    >>> print(format("select sum(a) over (partition by b) from t"))
    SELECT
        sum(a) over (partition by b)
    FROM
        t

    >>> print(format("select sum(a) from t group by b"))
    SELECT
        sum(a)
    FROM
        t
    GROUP BY
        b
    """
    return Format(query=query).run()


class Format:
    def __init__(self, query: str):
        self.reserved_words = ["select", "from", "group by", "SELECT", "FROM", "GROUP BY"]
        self.split_words = ["select", "from", ".*,", "group by"]
        self.query = self.generate_query_list(query)


    def generate_query_list(self, query: str) -> List[str]:
        def reserved_word2uppercase(word):
            if word in self.reserved_words:
                result_word = word.upper()
            else:
                result_word = word

            return result_word

        def split_query(query):
            return [val for val in re.split("(" + "|".join(self.split_words) + ")", query) if val != ""]

        splited_query = split_query(query)
        return [reserved_word2uppercase(word) for word in splited_query]

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
