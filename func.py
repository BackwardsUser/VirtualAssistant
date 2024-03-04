import time
import random


def swap_timezone(hour, modifier):
    """Swaps the hour to a new timezone considering positive or negative modifiers.

    Args:
        hour: The hour in the original timezone (0-23).
        modifier: The modifier to apply to the hour (+/- format).

    Returns:
        The hour in the new timezone (0-23).
    """

    new_hour = (hour + int(modifier)) % 24
    return new_hour


def to_twelve_hour(t):
    """Converts a 24-hour time format to a 12-hour time format.

    Args:
        t: An integer between 0 and 24 representing the hours in 24-hour format.
        m: An integer between 0 and 60 representing the minutes

    Returns:
        A string representing the time in 12-hour format with AM or PM appended.
    """

    if t == 0:
        return 12
    if t == 12:
        return 12
    if t < 12:
        return t
    return t-12


def minutes_to_phrase(hr, mins):
    """
    Converts minutes into a time phrase (e.g., 15 -> "quarter past", 30 -> "half past").

    Args:
        hr: An integer representing the hour.
        mins: An integer representing the minutes past the hour.

    Returns:
        A string representing the time phrase.
    """

    if 50 < mins < 60:
        minutes = 50
    elif mins >= 15 and mins != 45:
        minutes = round(mins, -1)
    else:
        minutes = mins

    if minutes == 0:
        return f"{hr} o'clock"
    if minutes == 15:
        return f"quarter past {hr}"
    if minutes == 30:
        return f"half past {hr}"
    if minutes == 45:
        return f"quarter to {hr}"
    if minutes < 30:
        return f"{minutes} past {hr}"
    return f"{60 - minutes} to {hr}"


def get_time():
    t = time.gmtime()

    intimezone = swap_timezone(t.tm_hour, -5)
    hours = to_twelve_hour(intimezone)
    out_time = minutes_to_phrase(hours, t.tm_min)

    return str(out_time)


def get_phrase(file):
    f = open(file, "r")
    phrases = []
    for x in f:
        phrases.append(x)
    phrase = phrases[random.randint(0, len(phrases))]
    print(phrase)
    return phrase


def all_phrase_banks(files):
    sentences = []
    for file in files:
        f = open(file, "r")
        for phrase in f:
            sentences.append(phrase)
    return sentences
