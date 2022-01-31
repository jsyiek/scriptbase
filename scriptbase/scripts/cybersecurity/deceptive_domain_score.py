import argparse
import logging
import os
import re

from typing import Iterator, List, Tuple

from scriptbase import SCRIPTBASE_DIRECTORY
import scriptbase.utils.algorithms.edit_distance as edit_distance
import scriptbase.utils.file_handling.file_utils as file_utils


REPEATED_NONALPHANUMERIC_CHARACTERS = r"(([^a-zA-Z\d\s:])\2)"
UNNECESSARY_NUMBERS_PATTERN = r"([\d]){3,}"
HTTP_HTTPS_PATTERN = r"(^https:\/\/www\.)|(^http:\/\/www\.)|(^https:\/\/)|(^http:\/\/)|(^www\.)"

this_logger = logging.getLogger(__name__)

def parse_args():

    parser = argparse.ArgumentParser(description="Computes the deceptive domain score for a given domain.")

    parser.add_argument("-d", "--domain", help="Domain name to compute score for", required=True)
    parser.add_argument("-c", "--company-data", help="Path to a CSV file containing company data to compare against. "
                                                     "Two columns required (no headers): second-level domain and "
                                                     "top-level domain",
                        default=os.path.join(SCRIPTBASE_DIRECTORY, "examples/demo_files/company_data.csv"))
    parser.add_argument("-q", "--quiet", help="Significantly reduces logging output; "
                                              "just prints the score", action="store_true")
    parser.add_argument("--see-closest-match", help="Shows the closest match even when the score is below "
                                                    "the threshold.", action="store_true")
    parser.add_argument("--threshold", help="Sets the threshold for declaring a website worthy of further review. "
                                            "Defaults to 5.", default=5, type=int)

    return parser.parse_args()


def clean_input(website_url: str) -> Tuple[str, list]:
    """
    Cleans an input domain name to remove any extra details that might be intended
    to fool a deceptive domain score

    Parameters:
        website_url (str): Domain name to clean

    Returns:
        Tuple[str, list]: Tuple of the cleaned string and a set of steps that are in similar
                          form to the output of edit_distance.visualize_steps if any
                          changes are made
    """

    # Removes http(s)://www. from the start of the website
    cleaned_domain = re.sub(HTTP_HTTPS_PATTERN, "", website_url)

    # Non-alphanumeric characters are rare in domain names but add unnecessary noise to the score.
    # we remove any that are not strictly numbers or digits
    # E.g. removing '-' from face-book.com
    # Removes all non-alphanumeric characters.
    cleaned_domain = re.sub(REPEATED_NONALPHANUMERIC_CHARACTERS, "", cleaned_domain)

    # the 0s in face0000000book.com add unnecessary noise to the score, so we remove the extraneous 0s
    # to get a better understanding of what the domain really is.
    # Removes any 3 consecutive numbers from the domain name. It's rare that there are three numbers in a
    # legitimate domain name (at least from my memory)
    cleaned_domain = re.sub(UNNECESSARY_NUMBERS_PATTERN, "", cleaned_domain)

    if website_url != cleaned_domain:
        return cleaned_domain, [("Removing obfuscating characters", f"{website_url} -> {cleaned_domain}")]
    return cleaned_domain, []


def tokenize(string_to_tokenize: str, length: int) -> Iterator[str]:
    """
    Generates all tokens of size length that can be created by contiguous sub-strings
    of string_to_tokenize

    Parameters:
         string_to_tokenize (str): String to generate contiguous tokens of size length from
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


def phish_target_score(domain_to_check: Tuple[str, str],
                       company_data: List[Tuple[str, str]]) -> Tuple[float, Tuple[str, str]]:
    """
    Computes the phish target score of an ordered domain tuple consisting of:
        1) second-level domain
        2) top-level domain

    ...against a company data consisting of a list of tuples that consist of the same elements

    Scoring mechanism:
    1) Begin with a score of 10
    2) Weight by the minimum edit distance from a given site.
        a) `edit_distance_weightings parameters correspond to specific edit distances and multiply the score by
           that amount.
    3) Weight by the proportion that the company name occupies in the domain name
        a) `subsection_size_weighting` is the amount that the proportion is raised to.
        b) This proportion is assumed to be <= 1, so we take the minimum of 1/company_name_proportion and
           company_name_proportion where company_name_proportion is len(company_name)/len(domain)
    4) Weight by whether or not the domain to check is a .com domain
        a) A domain may be less suspicious if it is a .com domain
    5) Weight by whether or not the domain to check has the same top-level domain as the potential target
        a) If impersonating a domain, it adds false legitimacy to have the same top-level domain

    Parameters:
        domain_to_check (Tuple[str, str]): Domain to compute phish target score for
        company_data (List[Tuple[str, str]]): List of company domains that might be targeted for phishing

    Returns:
        Tuple[float, Tuple[str, str]]: Tuple of floating point score from 0 to 10 describing phish target score
                                       and the closest company matched
    """
    # TODO: Make parameters configurable
    edit_distance_weightings = {0: 1.2, 1: 1.1, 2: 0.5}
    subsection_size_weighting = 0.6
    top_level_domain_same_weightings = {True: 1, False: 0.9}
    top_level_domain_is_com = {True: 0.8, False: 1}

    # This key function implements the scoring metrics (see doc string for explanation)
    # to ensure that the largest score is chosen from the possible scores
    def calculate_score(company: tuple, edit_data_tuple: tuple) -> float:

        company_name_proportion = len(company[0])/len(domain_to_check[0])

        score = 10
        score *= edit_distance_weightings.get(edit_data_tuple[0], 0)
        score *= min(company_name_proportion, 1/company_name_proportion) ** subsection_size_weighting
        score *= top_level_domain_same_weightings[domain_to_check[1] == company[1]]
        score *= top_level_domain_is_com[domain_to_check[1] == "com"]

        return min(score, 10)

    # Generator for (company_tuple, (edit_distance, token))
    # (for an explanation of the latter part of tuple, see minimum_token_edit_distance)
    comparisons = ((company, minimum_token_edit_distance(domain_to_check[0], company[0])) for company in company_data)
    closest_company_match, (distance, token) = max(comparisons, key=lambda t: calculate_score(*t))

    return calculate_score(closest_company_match, (distance, token)), closest_company_match


def string_entropy_score(domain_to_check: Tuple[str, str]) -> float:
    """
    Not implemented yet
    """

    return 0.0


def main():

    args = parse_args()

    domain, steps = clean_input(args.domain)
    domain = domain.split(".", 1)

    if len(domain) < 2:
        this_logger.critical(f"Domain must contain only second-level and top-level domain! E.g. google.com")
        exit()

    if "." in domain[1]:
        this_logger.warning(f"Assuming that {domain[1]} is a top-level domain!")

    try:
        company_data = file_utils.get_csv_contents(args.company_data)
    except FileNotFoundError as e:
        this_logger.critical(f"Path does not exist: {args.company_data}")
        exit()

    score, closest_company_matched = phish_target_score(domain, company_data)
    score = round(score, 2)

    if args.quiet:
        print(score)
        exit()

    this_logger.info(f"Score: {score}")
    prompt_further_review = score >= args.threshold
    this_logger.info(f"Prompt for further review? : {'Yes' if prompt_further_review else 'No'}")

    if prompt_further_review or args.see_closest_match:
        distance, further_steps = edit_distance.describe_edit_distance(domain[0], closest_company_matched[0])
        steps += edit_distance.visualize_steps(domain[0], further_steps)
        steps.append(("Matches: ", f"'{closest_company_matched[0]}'"))

        for step, i in zip(steps, range(1, len(steps) + 1)):
            this_logger.info(f"{i}) {step[0]}: {step[1]}")

if __name__ == "__main__":
    main()
