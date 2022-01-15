from typing import List, Tuple


def numeric_edit_distance(a: str, b: str) -> int:
    """
    Computes the Levenshtein distance between two strings

    Parameters:
        a (str): String to compare
        b (str): String to compare

    Returns:
        int: Levenshtein distance between a and b
    """

    dynamic_values = {}

    def numeric_edit_distance_dynamic(x: str, y: str):
        """
        Helper function that allows for the dynamic programming implementation
        of the Levenshtein distance
        """

        if (x, y) in dynamic_values:
            return dynamic_values[(x, y)]

        if not x:
            return len(y)
        if not y:
            return len(x)

        if x[0] == y[0]:
            dynamic_values[(x, y)] = numeric_edit_distance_dynamic(x[1:], y[1:])
            return dynamic_values[(x, y)]

        val1 = numeric_edit_distance_dynamic(x, y[1:])
        val2 = numeric_edit_distance_dynamic(x[1:], y)
        val3 = numeric_edit_distance_dynamic(x[1:], y[1:])

        dynamic_values[(x, y)] = 1 + min(val1, val2, val3)
        return dynamic_values[(x, y)]

    for str_len in range(1, max(len(a), len(b))):
        numeric_edit_distance_dynamic(a[0:str_len], b[0:str_len])

    return numeric_edit_distance_dynamic(a, b)


def describe_edit_distance(a: str, b: str) -> Tuple[int, tuple]:
    """
    Computes the steps needed to transform a to b and returns
    a tuple containg the Levenshtein distance in the first
    index and a tuple of steps to transform a to b in the
    second.

    Each step consist of three parts: a command, a character, and an index

    Commands:
    + -> Insertion (Character is the character being added)
    - -> Deletion (Character is the character being remove)
    * -> Substitution (Character is the character being substituted)

    E.g. ("+", "a", 0)

    The index of a particular step assumes all previous steps have already been processed

    Parameters:
        a (str): Starting string
        b (str): Target string

    Returns:
        Tuple[int, tuple]: Ordered tuple of 1) Levenshtein distance and 2) tuple
                           of steps to transform a to b
    """

    dynamic_values = {}

    def add_step(edit_data_list: tuple, next_step: tuple = None) -> tuple:
        """
        Helper function that adds a given step to the number of steps
        to transform a string x into a string y
        The next step can be None, indicating that no change was needed
        at this particular index. In this case, the edit indexes of each
        previous step is incremented.
        """

        increase_amount = 1 if next_step is None or next_step[0] != "-" else 0
        new_list = []

        if next_step is not None:
            new_list.append(next_step)
            total_steps = edit_data_list[0] + 1
        else:
            total_steps = edit_data_list[0]

        for previous_step in edit_data_list[1]:
            if previous_step[2] != -1:
                new_list.append((*previous_step[0:2], previous_step[2] + increase_amount))
            else:
                new_list.append(previous_step)

        return total_steps, tuple(new_list)

    def descriptive_edit_distance_dynamic(x: str, y: str):
        """
        Helper function that allows for the dynamic programming implementation
        of the Levenshtein distance.

        It calculates the conversion of x into y
        """

        if (x, y) in dynamic_values:
            return dynamic_values[(x, y)]

        # Base cases where x or y has been reduced to emptiness
        if not x:
            remaining_steps = tuple(("+", missing_char, i) for missing_char, i in zip(y, range(len(y))))
            dynamic_values[(x, y)] = (len(remaining_steps), remaining_steps)
            return dynamic_values[(x, y)]
        if not y:
            remaining_steps = tuple(("-", extra_char, 0) for extra_char in x)
            dynamic_values[(x, y)] = (len(remaining_steps), remaining_steps)
            return dynamic_values[(x, y)]

        # First two characters are the same so no need to change anything
        # Can progress to next value
        if x[0] == y[0]:
            dynamic_values[(x, y)] = add_step(descriptive_edit_distance_dynamic(x[1:], y[1:]))
            return dynamic_values[(x, y)]

        # Adding first element of y to x
        val1 = add_step(descriptive_edit_distance_dynamic(x, y[1:]), ("+", y[0], 0))

        # Deleting first element of x
        val2 = add_step(descriptive_edit_distance_dynamic(x[1:], y), ("-", x[0], 0))

        # Changing first element of x to that of y
        val3 = add_step(descriptive_edit_distance_dynamic(x[1:], y[1:]), ("*", y[0], 0))

        dynamic_values[(x, y)] = min(val1, val2, val3, key=lambda t: t[0])

        return dynamic_values[(x, y)]

    for str_len in range(1, max(len(a), len(b))):
        descriptive_edit_distance_dynamic(a[0:str_len], b[0:str_len])

    return descriptive_edit_distance_dynamic(a, b)


def collapse_steps(steps: Tuple[Tuple[str, str, int]]) -> Tuple[Tuple[str, str, tuple]]:
    """
    Collapses a set of steps from descriptive_edit_distance by combining
    all steps with the same command that act on adjacent indexes

    For example: (("+", "a", 0), ("+", "b", 1)) would be collapsed to ("+", "ab", (0, 2))

    Parameters:
        steps (Tuple[Tuple[str, str, int]]): A tuple of steps from descriptive_edit_distance

    Returns:
        Tuple[Tuple[str, str, tuple]]: Input steps collapsed to a new object as described above
    """

    if not steps:
        return ()

    def collapse(data: List[Tuple[str, str, int]]) -> Tuple[str, str, tuple]:
        """
        Short helper function that is used to collapse the data from previous_steps
        into a single step with a ranged index describing over what indexes it operates
        """
        combined_string = "".join(s[1] for s in data)

        if data[0][0] == "-":
            index_range = (data[0][2], data[0][2] + len(data))
        else:
            index_range = (data[0][2], data[-1][2] + 1)

        return data[0][0], combined_string, index_range

    shortened_steps = []

    # Maintain a buffer of previous steps to be able to collapse them
    previous_steps = [steps[0]]

    for step in steps[1:]:

        # We only want to collapse steps of the same type
        if step[0] == previous_steps[-1][0]:

            # Deletion indexes work slightly differently since the
            # next deletion step assumes the previous one has already been applied
            if step[0] == "-" and previous_steps[-1][2] == step[2]:
                previous_steps.append(step)
            elif step[0] in ("+", "*") and previous_steps[-1][2] + 1 == step[2]:
                previous_steps.append(step)
            else:
                shortened_steps.append(collapse(previous_steps))
                previous_steps = [step]

        else:
            shortened_steps.append(collapse(previous_steps))
            previous_steps = [step]

    # Deal with anything left in the buffer
    shortened_steps.append(collapse(previous_steps))

    return shortened_steps


def visualize_steps(starting_string: str, steps: Tuple[Tuple[str, str, int]]) -> List[Tuple[str, str]]:
    """
    Generates a list of ordered tuples containing:
        1) Written description of command
        2) Command visualized, surrounding change with <>

    For example: (("+", "a", 0), ("+", "b", 1)) on the string "cd" would create:
    [("Add 'ab'", "<ab>cd")]

    Parameters:
        starting_string (str): String that the steps are modifying
        steps (Tuple[Tuple[str, str, int]]): Steps data from edit_distance_dynamic

    Returns:
        List[Tuple[str, str]]: List of ordered-tuples representing the changes
    """

    # Collapse the steps so that the return can be represented clearer
    # This means the index of modification is an ordered 2-tuple
    steps = collapse_steps(steps)

    variations = []
    current_modification = starting_string

    for step in steps:

        if step[0] == "+":
            modification = current_modification[0:step[2][0]] + f"<{step[1]}>" + current_modification[step[2][0]:]
            variations.append((f"Add '{step[1]}'", modification))
            current_modification = current_modification[0:step[2][0]] + step[1] + current_modification[step[2][0]:]

        elif step[0] == "-":
            modification = current_modification[0:step[2][0]] \
                           + f"<{step[1]}>" \
                           + current_modification[step[2][1]:]
            variations.append((f"Remove '{step[1]}'", modification))
            current_modification = current_modification[0:step[2][0]] \
                           + current_modification[step[2][1]:]

        elif step[0] == "*":
            modification = current_modification[0:step[2][0]] + f"<{step[1]}>" + current_modification[step[2][1]:]
            variations.append((f"Substitute '{current_modification[step[2][0]:step[2][1]]}' with '{step[1]}'",
                               modification))
            current_modification = current_modification[0:step[2][0]] + step[1] + current_modification[step[2][1]:]

    return variations
