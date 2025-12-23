"""
Purpose: A Service class that is responsible for converting integers to Roman numerals.
Attributes:
    VALUES (list[int]): Roman numeral base values in descending order.
    SYMBOLS (list[str]): Roman numeral symbols corresponding to VALUES.
"""

class RomanNumeralTranslateService:
    # Ordered Roman numeral values and symbols.
    # Order is critical: larger values and subtractive forms (e.g., 900 = CM)
    # must be evaluated first to generate canonical Roman numerals.
    VALUES = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    SYMBOLS = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

    def convert(self, number: int) -> str:
        """
        Purpose: Convert an integer to its Roman numeral representation.
        Args: number (int): Integer to convert. Must be in the range 1 to 255.
        Returns: a str of Roman numeral that representation conversion of the input number.
        Raises: a ValueError If the input number is outside the supported range.
        """

        # Fail fast on invalid input to keep downstream logic simple and prevent undefined Roman numeral representations.
        if number < 1 or number > 255:
            raise ValueError("Input must be between 1 and 255")

        result: list[str] = []
        remaining = number

        # Greedy conversion algorithm:
        # Repeatedly subtract the largest possible Roman value until the entire number has been converted.
        for value, symbol in zip(self.VALUES, self.SYMBOLS):
            while remaining >= value:
                result.append(symbol)
                remaining -= value

        # Join once at the end for efficiency
        return "".join(result)
