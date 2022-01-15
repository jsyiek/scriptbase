from typing import List, Iterator, Tuple

import scriptbase.utils.algorithms.edit_distance as edit_distance


def tokenize(string_to_tokenize: str, length: int) -> Iterator[str]:
    """
    Generates all tokens of size length that can be created by contiguous sub-strings
    of string_to_tokenize

    Parameters:
         string_to_tokenize (str): String to generate contingous tokens of size length from
         length (int): Size of token to generate

    Yields:
        str: Token of size length
    """

    for offset in range(0, max(1, len(string_to_tokenize) - length + 1)):
        yield string_to_tokenize[offset:offset + length]


def minimum_token_edit_distance(second_level_domain: str,
                                company_to_compare: str,
                                lenience: int = 2) -> Tuple[int, str]:
    """
    Calculates the minimum Levenshtein distance for all tokens of second_level_domain of length
    equal to the length of company_to_compare +/- the lenience

    The lenience allows extra characters to be added to the second_level_domain
    relative to company_to_compare and still read an accurate edit score over a section.

    For example, "american-express-update" is clearly based on "americanexpress" but would
    return an edit distance of 2 for the comaprison of "american-expres" and "americanexpress"
    when the better comparison of "american-express" and "americanexpress" returns 1 - this would require
    a lenience of at least 1.

    Parameters:
        second_level_domain (str): Second-level domain name to check
        company_to_compare (str): Company to check the second level domain name against
        lenience (int): Amount of length to fudge the token length by to allow for more accurate edit distance
                        calculation. Assumed to be positive. Defaults to 2

    Returns:
        Tuple[int, str]: Tuple containing the minimum edit distance found alongside the token that created it
    """

    lenience = abs(lenience)

    # Generators a list of iterators
    # Each iterator generates the valid tokens for a given length +/- the lenience
    token_iterators = (tokenize(second_level_domain, len(company_to_compare) + fudge)
                       for fudge in range(-lenience, lenience + 1))

    # Generates a list of lists of tuple pair of (edit_distance: int, token: str)
    # The token is returned alongside the int to allow description to the user of what is causing the low edit distance
    # Each list in the list of lists represents the tokens of a different fudged length
    edit_distance_list = ([(edit_distance.numeric_edit_distance(token, company_to_compare), token)
                           for token in token_it]
                          for token_it in token_iterators)

    flattened_edit_distance_list = sum(edit_distance_list, [])

    return min(flattened_edit_distance_list, key=lambda t: t[0])


if __name__ == "__main__":
    starting_string = "Doctor Strange"
    target_string = "Strange Supreme"
    distance, steps = edit_distance.describe_edit_distance(starting_string, target_string)
    print(edit_distance.visualize_steps(starting_string, steps))
    # print(edit_distance.collapse_steps(edit_distance.describe_edit_distance("DStrange", "Strange")[1]))
    # print(edit_distance.describe_edit_distance("american-express", "americanexpress"))
    # print(edit_distance.numeric_edit_distance("americanexpress", "american-express"))
    # import datetime
    # now = datetime.datetime.now()
    # print(minimum_token_edit_distance("ebay-update", "ebay"))
    # print(datetime.datetime.now() - now)
