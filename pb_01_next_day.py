"""Provide a function to obtain the next day after a given date.

Examples of use:
>>> next_date('1-7-2024')
'2-7-2024'

>>> next_date('28-7-2024')
'29-7-2024'
>>> next_date('29-7-2024')
'30-7-2024'
>>> next_date('30-7-2024')
'31-7-2024'
>>> next_date('31-7-2024')
'1-8-2024'

>>> next_date('28-9-2024')
'29-9-2024'
>>> next_date('29-9-2024')
'30-9-2024'
>>> next_date('30-9-2024')
'1-10-2024'

>>> next_date('28-2-2024')
'29-2-2024'
>>> next_date('29-2-2024')
'1-3-2024'

>>> next_date('28-2-2025')
'1-3-2025'

>>> next_date('31-12-2024')
'1-1-2025'

>>> next_date('0-7-2024')
Traceback (most recent call last):
...
ValueError: Day must be between 1 and 31.

>>> next_date('32-7-2024')
Traceback (most recent call last):
...
ValueError: Day must be between 1 and 31.
>>> next_date('31-9-2024')
Traceback (most recent call last):
...
ValueError: Day must be between 1 and 30.
>>> next_date('30-2-2024')
Traceback (most recent call last):
...
ValueError: Day must be between 1 and 29.
>>> next_date('29-2-2025')
Traceback (most recent call last):
...
ValueError: Day must be between 1 and 28.

>>> next_date('30-0-2024')
Traceback (most recent call last):
...
ValueError: Month must be between 1 and 12.
>>> next_date('30-13-2024')
Traceback (most recent call last):
...
ValueError: Month must be between 1 and 12.

>>> next_date('1-7-1582')
Traceback (most recent call last):
...
ValueError: Year must be greater than 1582.

>>> next_date('1-7-2024-12-00-00')
Traceback (most recent call last):
...
ValueError: Wrong format
>>> next_date('1-7')
Traceback (most recent call last):
...
ValueError: Wrong format

>>> next_date('1/7/2024')
'2-7-2024'
>>> next_date('1.7.2024')
'2-7-2024'
"""


def next_date(dt):
    """The only function of the module"""
    tks = dt.replace("/", "-").replace(".", "-").split("-")
    if len(tks) != 3:
        raise ValueError("Wrong format")
    y = int(tks[2])
    if y <= 1582:
        raise ValueError("Year must be greater than 1582.")
    m = int(tks[1])
    if m < 1 or m > 12:
        raise ValueError("Month must be between 1 and 12.")
    t = 31
    if m == 2:
        if y % 400 == 0:
            t = 29
        elif y % 100 == 0:
            t = 28
        elif y % 4 == 0:
            t = 29
        else:
            t = 28
    elif m in (4, 6, 9, 11):
        t = 30
    d = int(tks[0])
    if d < 1 or d > t:
        raise ValueError("Day must be between 1 and " + str(t) + ".")
    d += 1
    if d > t:
        d = 1
        m += 1
        if m > 12:
            m = 1
            y += 1
    return "-".join([str(d), str(m), str(y)])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
