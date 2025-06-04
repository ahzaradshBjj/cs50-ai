import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # When # of cells equals the count, we know that these are mines
        if len(self.cells) == self.count:
            return self.cells
        # returns an empty set
        return set()

        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # when count is 0, all are safe
        if not self.count:
            return self.cells
        # returns an empty set when we can not conclude anything
        return set()

        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if mine is in the sentence, update sentence so that cell is no longer in the sentence
        if cell in self.cells:
            self.cells.remove(cell)
            # we decrease the count (how many mines there are) since we already know that cell is a mine
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if safe cell is in the sentence, update sentence so that cell is no longer in the sentence
        if cell in self.cells:
            self.cells.remove(cell)
            # we do not decrease the count because the cell removed is not a mine


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1
        self.moves_made.add(cell)

        # 2
        self.mark_safe(cell)

        # 3
        neighbors = set()

        # Loop through one neighboring cell
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore cell itself
                if (i, j) == cell:
                    continue
                # Make sure you do not go out of bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        count -= 1
                    # Undertermined cells
                    elif (i, j) not in self.safes:
                        neighbors.add((i, j))

        if neighbors:
            self.knowledge.append(Sentence(neighbors, count))

        # 4 and 5
        self.update_knowledge()

        # cells = set()
        # # I need to loop through one neighboring cell
        # for i in range(cell[0] - 1, cell[0] + 2):
        #     for j in range(cell[1] - 1, cell[1] + 2):

        #         # ignore cell itself
        #         if (i, j) == cell:
        #             continue

        #         # make sure you do not go out of bounds
        #         if 0 <= i < self.height and 0 <= j < self.width:
        #             # if cell is not a move that has already been made and not a mine
        #             if (i, j) not in self.moves_made and (i, j) not in self.mines:
        #                 cells.add((i, j))
        #             # when we know the cell is a mine
        #             elif (i, j) in self.mines:
        #                 count -= 1

        # self.knowledge.append(Sentence(cells, count))

        # 4
        # # iterate through all sentence
        # for sentence in self.knowledge:
        #     # get safes ones
        #     safes = sentence.known_safes()
        #     if safes:
        #         for cell in safes.copy():
        #             # mark as safes
        #             self.mark_safe(cell)
        #     # get mines
        #     mines = sentence.known_mines()
        #     if mines:
        #         for cell in mines.copy():
        #             # mark as mines
        #             self.mark_mine(cell)

        # 5
        # for sentence1 in self.knowledge:
        #     for sentence2 in self.knowledge:
        #         if sentence1 is sentence2:
        #             continue
        #         if sentence1 == sentence2:
        #             self.knowledge.remove(sentence2)
        #         elif sentence1.cells.issubset(sentence2.cells):
        #             new_knowledge = Sentence(
        #                 sentence2.cells - sentence1.cells,
        #                 sentence2.count - sentence1.count)
        #             if new_knowledge not in self.knowledge:
        #                 self.knowledge.append(new_knowledge)

    def update_knowledge(self):
        """
        Updates the AI's knowledge base to mark new cells as safe or as
        mines based on the current knowledge
        """

        changed = True

        while changed:
            changed = False
            new_mines = set()
            new_safes = set()

            for sentence in self.knowledge:
                # Identify new mines and safes
                known_mines = sentence.known_mines()
                known_safes = sentence.known_safes()

                if known_mines:
                    new_mines.update(known_mines)
                    
                if known_safes:
                    new_safes.update(known_safes)

            for mine in new_mines:
                if mine not in self.mines:
                    self.mark_mine(mine)
                    changed = True

            for safe in new_safes:
                if safe not in self.safes:
                    self.mark_safe(safe)
                    changed = True

            # Get non empty cells
            self.knowledge = [s for s in self.knowledge if s.cells]

        new_sentences = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2 and sentence2.cells.issubset(sentence1.cells) and sentence2.cells:
                    new_cells = sentence1.cells - sentence2.cells
                    new_count = sentence1.count - sentence2.count

                    if new_count >= 0:
                        inferred_sentence = Sentence(new_cells, new_count)
                        if inferred_sentence not in self.knowledge and inferred_sentence not in new_sentences:
                            new_sentences.append(inferred_sentence)
                            changed = True

        self.knowledge.extend(new_sentences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for c in self.safes:
            if c not in self.moves_made:
                return c
        return None
        # steps = self.safes.difference(self.moves_made)
        # if steps:
        #     return random.choice(tuple(steps))
        # return None
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # # if no move can be made
        # if len(self.mines) + len(self.moves_made) == self.height * self.width:
        #     return None

        # # loop until an appropriate move is found
        # while True:
        #     i = random.randrange(self.height)
        #     j = random.randrange(self.width)
        #     if (i, j) not in self.moves_made and (i, j) not in self.mines:
        #         return (i, j)

        # generate all possible cells we can work on
        all_cells = set(itertools.product(range(self.height), range(self.width)))
        # get all the possible moves
        possible_moves = list(all_cells - self.moves_made - self.mines)

        # if there are possible moves
        if possible_moves:
            return random.choice(possible_moves)
        else:
            return None
