import json
import os


class Sudoku:
    def __init__(self, data):
        self.board = data
        self.fixed = self.get_fixed_cells()

    def __repr__(self):
        repr = ""

        n = 0
        for row in self.board:
            for cell in row:
                if cell == 0:
                    repr += "  "
                else:
                    if n in self.fixed:
                        repr += "\033[92m" + str(cell) + " \033[0m"
                    else:
                        repr += str(cell) + " "
                n += 1
            repr = (repr + "\n") if n < 81 else repr + ""

        return repr

    def __getitem__(self, index):
        if index < 0 or index > 80:
            raise IndexError(f"index ({index}) out of range")
        return self.board[int(index/9)][index % 9]

    def __setitem__(self, index, value):
        if index < 0 or index > 80:
            raise IndexError(f"index ({index}) out of range")
        self.board[int(index/9)][index % 9] = value

    def get_fixed_cells(self):
        fixed = []

        n = 0
        for row in self.board:
            for cell in row:
                if cell != 0:
                    fixed.append(n)
                n += 1

        return fixed

    def check(self):

        for row in self.board:
            for i in range(1, 10):
                if row.count(i) > 1:
                    return False

        for n in range(9):
            col = []
            for row in self.board:
                col.append(row[n])
            for i in range(1, 10):
                if col.count(i) > 1:
                    return False

        boxes_indices = [
            [(i, j) for i in range(3) for j in range(3)],
            [(i, j) for i in range(3, 6) for j in range(3)],
            [(i, j) for i in range(6, 9) for j in range(3)],
            [(i, j) for i in range(3) for j in range(3, 6)],
            [(i, j) for i in range(3, 6) for j in range(3, 6)],
            [(i, j) for i in range(6, 9) for j in range(3, 6)],
            [(i, j) for i in range(3) for j in range(6, 9)],
            [(i, j) for i in range(3, 6) for j in range(6, 9)],
            [(i, j) for i in range(6, 9) for j in range(6, 9)],
        ]

        for box_indices in boxes_indices:
            box = []
            for index in box_indices:
                box.append(self.board[index[0]][index[1]])
            for i in range(1, 10):
                if box.count(i) > 1:
                    return False

        return True

    def all_filled(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True


def switch_console_font_size():
    font_increase = 30

    with open("settings.json", "r") as f:
        settings = json.load(f)

    if settings["terminal.integrated.fontSize"] == 14:
        settings["terminal.integrated.fontSize"] += font_increase
    else:
        settings["terminal.integrated.fontSize"] -= font_increase

    with open("settings.json", "w") as f:
        json.dump(settings, f)


def main():
    # Switch console font size
    switch_console_font_size()

    # Get the input data for the sudoku
    with open("sudoku.txt") as f:
        data = f.readlines()

    # Format the data for further usage
    data = [item.strip().replace("-", "0").split(" ") for item in data]
    data = [[int(item) for item in sub_list] for sub_list in data]

    # Create a sudoku instance
    sudoku = Sudoku(data)

    # Run a backtracking algorithm to find a solution
    i = 0
    backtracking = False
    counter = 0
    while True:
        counter += 1
        if counter % 50 == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(sudoku)

        if sudoku.all_filled() and sudoku.check():
            break

        if i in sudoku.fixed:
            i = i-1 if backtracking else i+1
        else:
            if sudoku[i] == 9:
                sudoku[i] = 0
                i -= 1
                backtracking = True
                continue
            else:
                sudoku[i] += 1

            if sudoku.check():
                i += 1
                backtracking = False

    # Save the solved sudoku in a new file
    with open("solution.txt", "w") as f:
        solved_sudoku = ""

        for row in sudoku.board:
            for cell in row:
                solved_sudoku += str(cell) + " "
            solved_sudoku += "\n"

        f.write(solved_sudoku)

    # In addition, print the sudoku in the console
    os.system('cls' if os.name == 'nt' else 'clear')
    print(sudoku)

    # Change back the font size
    switch_console_font_size()


if __name__ == "__main__":
    main()
