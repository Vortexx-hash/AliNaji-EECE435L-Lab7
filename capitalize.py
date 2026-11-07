"""The capitalization exercise from Lab 7."""


def capital_case(x):
    """Capitalize a string, with the handout's friendly type error."""
    if not isinstance(x, str):
        raise TypeError("Please provide a string argument")
    return x.capitalize()
