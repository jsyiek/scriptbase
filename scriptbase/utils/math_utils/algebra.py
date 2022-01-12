from typing import List


class BaseFunction:

    def __init__(self, function_str: str):
        """
        Parameters:
            function_str (str): String with regex matching to find argument (optionally)
        """

        self.function_str = function_str
        self.argument = ""

    def generate_instance(self, function: str):
        """
        Parameters:
            function (str): The instance of the function
        """