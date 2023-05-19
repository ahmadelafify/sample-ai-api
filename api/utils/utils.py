import math


def censor_string(value: str) -> str:
    slice_count = 5
    value_length = len(value)
    if value_length < 3:
        return ''.join(['*' * value_length])
    show_amount = min(slice_count, value_length)
    show_count = math.floor(value_length/show_amount)
    hidden_count = math.floor(value_length - show_count) - 1
    return f"{value[:show_count]}{''.join(['*' * hidden_count])}{value[(show_count*-1):]}"