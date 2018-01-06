from sys import argv

class Billboard:
    def __init__(self, line):
        fields = line.split(' ')
        self.width = int(fields[0])
        self.height = int(fields[1])
        # We only need to care about lengths of words
        self.word_lengths = [len(s.rstrip()) for s in fields[2:]]

    def __fits(self, font_size, number_of_lines, index):
        '''
        Checks if a message fits on a billboard with a given font size

        This function is meant to be called by fits. It recursively checks
        whether a certain font size fits on the billboard. The idea is to
        construct the longest line that fits on the billboard. Afterwards, the
        question is whether the rest of the string fits on the rest of the
        lines, hence the recursive call.

        Args:
            font_size (int): Candidate font size
            number_of_lines (int): How many lines are left on the billboard
            index (int): Index of the first word to be displayed

        Returns:
            bool: Does the message fit?
        '''
        if self.width == 0:
            return False
        if number_of_lines == 0:
            return False

        # Each time we add a word to a line, we need to add a space. Initialising
        # this variable to -font_size takes care of the case of the first word of
        # the line
        line_length = -font_size

        while line_length <= billboard.width:
            try:
                line_length += font_size * (self.word_lengths[index] + 1)
                index = index + 1
            except IndexError:
                return True

        # When we get out of the while loop, our line is too long. Hence the call
        # with index-1
        return self.__fits(font_size, number_of_lines - 1, index -1)

    def fits(self, font_size):
        '''
        Checks if a message fits on a billboard with a given font size

        Args:
            billboard (Billboard): The billboard and the text
            font_size (int): Font size to be tested
        Returns:
            bool: Does the message fit?
        '''
        if font_size == 0:
            return True
        return self.__fits(font_size, billboard.height // font_size, 0)


    def __max_font(self, lower_limit, upper_limit):
        '''
        Returns the maximum font size permissible.

        This function uses a binary search algorithm to find the maximum
        font size. There is nothing too clever about this otherwise.

        Args:
            lower_limit (int): A lower limit on the maximum font size
            upper_limit (int): An upper limit on the maximum font size
        Returns:
            int: maximum font size
        '''
        if lower_limit == upper_limit :
            return lower_limit
        if upper_limit - lower_limit == 1:
            return upper_limit if self.fits(upper_limit) else lower_limit
        mid = (lower_limit+upper_limit) // 2
        if self.fits(mid):
            return self.__max_font(mid, upper_limit)
        else:
            return self.__max_font(lower_limit, mid)

    def max_font(self):
        '''
        Returns the maximum font size permissible

        Returns:
            int: maximum font size
        '''

        # A simple way of getting an upper boundary on the maximum font
        # size is to consider that the longest word has to fit on a line
        upper_limit = self.width // max(self.word_lengths)
        return self.__max_font(0, upper_limit)

def read_file(file_name):
    '''
    Reads a file containing billboard dimensions and text

    This function expects an integer representing
    the number of lines to be read on the first line. All consequent lines are
    expected to be of the form
    Width Height String

    Args:
        file_name (str): Path to the input file

    Returns:
        Billboard: A list of billboards
    '''

    billboards = []
    with open(file_name, 'r') as f:
        number_of_lines = int(f.readline())
        for i in range(number_of_lines):
            billboards.append(Billboard(f.readline()))
    return billboards

if __name__ == "__main__":
    billboards = read_file(argv[1])
    for ind, billboard in enumerate(billboards):
        print("Case #{}: {}".format(ind+1, billboard.max_font()))
