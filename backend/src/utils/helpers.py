def round_float(number: float, decimal_places: int) -> float:
    """
    Rounds a float to the nearest decimal input.

    Arguments:
    -----------
    number : float
        Defines a floating number.
    decimal_places : int
        Defines the number of places after the comma to round the float.
    
    Returns:
    ---------
    float
    Example:
    ---------
    ```
    >>> round_float(3.52487,2) # Outputs: 3.52
    ```

    """
    return float(f"{number:.{decimal_places}f}")


def remove_decimals(amount: int, decimals: int, decimal_places: int):
    """
    Removes the specified amount of decimal places from the number.

    Arguments:
    -----------
    amount : int
        Defines a Integer number.
    decimals : int
        Defines the decimal part of a number 
    decimal_places : int
        Defines the number of places after the comma.

    
    Returns:
    ---------
    Returns a float truncated number.
    Example:
    ---------
    ```
    >>> remove_decimal(3.52887,2) # Outputs: 3.52
    ```
    """
    return round_float(number=amount * 10 ** (-decimals), decimal_places=decimal_places)


def add_decimals(amount: int, decimals: int):
    """
    Adds the decimal part of a number.

    Arguments:
    -----------
    amount : int
        Defines a Integer number.
    decimals : int
        Defines the amount of zeros to add for the integer.
    
    Returns:
    ---------
    int
    
    Example:
    ---------
    ```
    >>> add_decimal(3,2) # Outputs: 300
    ```
    """
    return int(amount * 10 ** (decimals))
