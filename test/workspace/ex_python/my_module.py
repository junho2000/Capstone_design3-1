def my_avg(x1, x2):
    """
    This function calculates average value of two numbers
    x1 : first input number
    x2 : second input number
    """
    if isinstance(x1, (int, float)) and isinstance(x2, (int, float)):
        avg_val = (float(x1) + float(x2)) / 2
        return avg_val
    else:
        print("This is not a number")
