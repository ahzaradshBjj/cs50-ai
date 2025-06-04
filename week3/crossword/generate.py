import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Every variable in a variable's domain has the same number of
        # letters as the variable's length (each variable in self.domain
        # is node consistent)

        # Iterate through variables in the domain
        for v in self.domains:
            # Iterate through domains
            for domain in self.domains[v].copy():
                # If length of domain is not the same as length
                # of variable, remove it
                if v.length != len(domain):
                    self.domains[v].remove(domain)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return False

        # Values i, j of the overlap
        i, j = overlap

        revised = False
        # For each domain in x
        for domain_x in self.domains[x].copy():
            # For each domain in y
            # If all domain_y do not meet condition, delete domain_x
            # if at least one does, do not delete it
            if all(domain_x[i] != domain_y[j] for domain_y in self.domains[y]):
                self.domains[x].remove(domain_x)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = []
            # Get all the variables
            for x in self.crossword.variables:
                # Get the neighbors of the variable (variables that overlap)
                for y in self.crossword.neighbors(x):
                    # Add variables and its neighbors (binary constraints)
                    # those are the arcs
                    arcs.append((x, y))

        queue = list(arcs)

        # Algorithm in the lecture
        while len(queue) > 0:
            # Get arc (variable and its neighbor)
            x, y = queue.pop(0)

            if self.revise(x, y):
                # If no more domains[x], no solution
                if len(self.domains[x]) == 0:
                    return False

                # Check each neighbor of x because there was a revise
                # the domain values of x changed
                for neighbor in self.crossword.neighbors(x):
                    # If the neighbor not equal to y
                    if neighbor != y:
                        queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Loop through each variable
        for var in self.crossword.variables:
            # If var not in the assignment
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment:
            # Assign the attempts of the variable
            word = assignment[var]

            # Check distinction of values(both keys and value)
            for other_var in assignment:
                # If any other_var is different (false at first)
                # if word == assignment[other_var] (true at first)
                if other_var != var and word == assignment[other_var]:
                    return False

            # Check length value
            if len(word) != var.length:
                return False

            # Iterate through each neighbor of the var
            for neighbor in self.crossword.neighbors(var):
                # We gotta find if neighbor is in the assignment
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    # It is not crutial, all neighbors overlap
                    if overlap:
                        i, j = overlap
                        if word[i] != assignment[neighbor][j]:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        conflicts = []

        # Iterate through each domain of the var
        # We know that var is not in the assignment since it is a
        # value that we try to find the least constraining value
        for domain in self.domains[var]:
            conflict_count = 0

            # If neighbor not in assignment, they must not be
            # we are supposed to find the neighbors that are
            # not in the assignment
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    # It is not crutial, all neighbors overlap
                    if overlap:
                        i, j = overlap
                        # Iterate through each domain of the neighbor
                        for word in self.domains[neighbor]:
                            # If domain of var not equal to domain of neighbor
                            if domain[i] != word[j]:
                                conflict_count += 1

            conflicts.append((domain, conflict_count))

        # Order in ascending order, considering the second element
        conflicts.sort(key=lambda x: x[1])

        return [value for value, _ in conflicts]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        best_var = None
        min_remaining_value = float("inf")
        max_degree = float("-inf")

        # If var not in assignment, they must not be
        # we are supposed to find the vars that are not already
        # in the assignment (find minimum remaining value)
        for var in self.crossword.variables:
            if var not in assignment:
                # Get the domains (values that var could take)
                remaining_values = len(self.domains[var])
                # How many neighbors does it have
                degree = len(self.crossword.neighbors(var))

                # Get min of remaining values
                if remaining_values < min_remaining_value:
                    best_var = var
                    min_remaining_value = remaining_values
                    max_degree = degree
                # Tie (highest degree)
                elif remaining_values == min_remaining_value:
                    if degree > max_degree:
                        best_var = var
                        max_degree = degree

        return best_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Algorithm in the lecture
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value

            if self.consistent(assignment):
                result = self.backtrack(new_assignment)

                if result:
                    return result

            del assignment[var]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
