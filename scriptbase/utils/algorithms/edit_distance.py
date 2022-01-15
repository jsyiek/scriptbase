__INCREASE_AMOUNTS = {"+" : 1, "*" : 1, "-" : 0}

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

    def edit_distance_dynamic(x: str, y: str):
        if (x, y) in dynamic_values:
            return dynamic_values[(x, y)]

        if not x:
            return len(y)
        if not y:
            return len(x)

        if x[0] == y[0]:
            dynamic_values[(x, y)] = edit_distance_dynamic(x[1:], y[1:])
            return dynamic_values[(x, y)]

        val1 = edit_distance_dynamic(x, y[1:])
        val2 = edit_distance_dynamic(x[1:], y)
        val3 = edit_distance_dynamic(x[1:], y[1:])

        dynamic_values[(x, y)] = 1 + min(val1, val2, val3)
        return dynamic_values[(x, y)]

    for str_len in range(1, max(len(a), len(b))):
        edit_distance_dynamic(a[0:str_len], b[0:str_len])

    return edit_distance_dynamic(a, b)


def describe_edit_distance(a: str, b: str) -> int:
    """
    Computes the steps needed to transform a to b

    + -> Insertion
    - -> Deletion
    * -> Substitution
    """

    dynamic_values = {}

    def add_step(edit_data_list: list, next_step: list = None) -> list:
        """
        Increments the index number of each index in the recorded steps, adds the new step to the front,
        and increments the number of steps in the front of the list.
        """

        increase_amount = 1 if next_step is None else __INCREASE_AMOUNTS[next_step[0]]
        for previous_step in edit_data_list[1]:
            if previous_step[2] != -1:
                previous_step[2] += increase_amount

        if next_step is not None:
            edit_data_list[1].insert(0, next_step)
            edit_data_list[0] += 1

        return edit_data_list

    def edit_distance_dynamic(x: str, y: str):
        if (x, y) in dynamic_values:
            return dynamic_values[(x, y)]

        if not x:
            remaining_steps = (["+", missing_char, -1] for missing_char in y)
            dynamic_values[(x, y)] = (len(remaining_steps), remaining_steps)
            return dynamic_values[(x, y)]
        if not y:
            remaining_steps = (["-", "", -1] for missing_char in x)
            dynamic_values[(x, y)] = (len(remaining_steps), remaining_steps)
            return dynamic_values[(x, y)]

        # First two characters are the same so change nothing
        if x[0] == y[0]:
            dynamic_values[(x, y)] = add_step(edit_distance_dynamic(x[1:], y[1:]))
            return dynamic_values[(x, y)]

        # Adding first element of y to x
        val1 = add_step(edit_distance_dynamic(x, y[1:]), ("+", y[0], 0))

        # Deleting first element of x
        val2 = add_step(edit_distance_dynamic(x[1:], y), ("-", "", 0))

        # Changing first element of x to that of y
        val3 = add_step(edit_distance_dynamic(x[1:], y[1:]), ("*", y[0], 0))

        dynamic_values[(x, y)] = min(val1, val2, val3, key=lambda t: t[0])
        if dynamic_values[(x, y)][1][0][0] == "*":
            breakpoint()

        return dynamic_values[(x, y)]

    for str_len in range(1, max(len(a), len(b)) + 1):
        edit_distance_dynamic(a[0:str_len], b[0:str_len])

        ## ISSUE IS WITH LISTS BEING MODIFIED BY REFERNECE

    print(dynamic_values)
    print(a, b)
    return edit_distance_dynamic(a, b)
