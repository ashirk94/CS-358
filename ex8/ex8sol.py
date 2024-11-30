# CS 358
# Alan Shirk - alans@pdx.edu
# Exercise 8: Types

# 1.
# (a)
def binary_operation() -> None:
    x = 4
    y = "string"
    result = x + y

# (b)
def string_function(string: str) -> str:
    return f"{string}"

def function_call() -> None:
    string_function(20)

# (c)
def assignment() -> None:
    num: int = "string"

# (d)
class City:
    def __init__(self, name):
        self.name = name

def class_field_access() -> None:
    portland = City("Portland")
    population = portland.population

# 2.
def division_by_zero() -> None:
    x = 2
    y = 0
    result = x / y

def index_out_of_range() -> None:
    my_list = [8, 9, 3]
    result = my_list[4]

# These runtime errors are not detected by mypy but are caught by python.
if __name__ == "__main__":
    try:
        division_by_zero()
    except Exception as e:
        print(f"Caught runtime error 1: {e}")

    try:
        index_out_of_range()
    except Exception as e:
        print(f"Caught runtime error 2: {e}")
