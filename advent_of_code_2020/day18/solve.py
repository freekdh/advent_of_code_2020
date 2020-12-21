from itertools import count
from collections import defaultdict
import numexpr
import re


def get_input_data(path_to_input_data):
    with open(path_to_input_data) as input_file:
        return input_file.read().splitlines()


class EquationEvaluator:
    def evaluate(self, equation: str):
        bracket_levels = self._get_bracket_levels(equation)
        for level, brackets in sorted(
            bracket_levels.items(), key=lambda item: item[1], reverse=True
        ):
            for bracket in brackets:
                evaluated_bracket = self._evaluate_left_to_right(
                    equation[bracket[0] + 1 : bracket[1]]
                )
                equation = (
                    equation[: bracket[0]]
                    + str(evaluated_bracket).rjust(bracket[1] - bracket[0] + 1, " ")
                    + equation[bracket[1] + 1 :]
                )
        return self._evaluate_left_to_right(equation)

    def _get_bracket_levels(self, equation):
        current_opening_brackets = []
        bracket_levels = defaultdict(list)
        for index, character in enumerate(list(equation)):
            if character == "(":
                current_opening_brackets.append(index)
            elif character == ")":
                level = len(current_opening_brackets)
                start_index = current_opening_brackets.pop()
                end_index = index
                bracket_levels[level].append((start_index, end_index))
        return bracket_levels

    def _evaluate_left_to_right(self, equation):
        equation = equation.replace(" ", "")
        start_digit = int(re.search(r"(\d+)", equation).group())
        operations = re.findall(r"([\*\+])(\d+)", equation)
        for operation in operations:
            if operation[0] == "+":
                start_digit += int(operation[1])
            elif operation[0] == "*":
                start_digit *= int(operation[1])
        return start_digit


def main():
    input_data = get_input_data("advent_of_code_2020/day18/input.txt")

    equation_evaluator = EquationEvaluator()

    sum_of_equations_homework = sum(
        equation_evaluator.evaluate(equation) for equation in input_data
    )

    print(f"Part1: {sum_of_equations_homework} is the sum of the resulting values")


if __name__ == "__main__":
    main()