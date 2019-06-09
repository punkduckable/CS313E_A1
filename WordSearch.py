#  File: WordSearch.py

#  Description: This program finds the locations of words in an rectangular
#  grid of letters.

#  Student Name: Robert Stephany

#  Student UT EID: rrs2558

#  Partner Name:

#  Partner UT EID:

#  Course Name: CS 313E

#  Unique Number: 85575

#  Date Created: 06/09/2019

#  Date Last Modified: 06/09/2019

################################################################################
# Functions to read in from file.

def remove_empty_elements(List):
    """This function removes empty elements from List. Even though lists are
    mutable, the processed list is returned to improve readability."""

    # Cycle through the list.
    i = 0;
    while i < len(List):
        # if the current cell is an empty string, remove it. Otherwise,
        # incremenet the counter.
        if(len(List[i]) == 0):
            del List[i];
        else:
            i = i+1;

    # Now remove the processed list.
    return List;



def remove_newline_characters(List):
    """As the name suggests, this function removes newline characters from
    list. To improve readibility, the procesed list is returned"""

    # Cycle through the list.
    list_length = len(List);
    for i in range(list_length):
        if ("\n" in List[i]):
            List[i] = List[i].replace("\n","");

    return List;



def read_in_file():
    """ This function reads in hidden.txt and processes it. The grid of letters
    is read into a 2d array while the desired words is read into a 1d list.
    Both of these lists are then returned. """

    File = open("hidden.txt","r");

    ############################################################################
    # First, read in m,n

    # First, determine the dimensions of the array.
    space_split_first_line = (File.readline()).split(" ");

    # Depending on how many spaces were used between n and m,
    # space_split_first_line could have any number of empty elements. Let's get
    # rid of those
    space_split_first_line = remove_empty_elements(space_split_first_line);

    # Now we can assign m and n
    m = int(space_split_first_line[0])
    n = int(space_split_first_line[1])


    ############################################################################
    # Next, find the character grid.
    # Read in each line of the file, turn it into a row of the character grid,
    # and then store that line in the character grid (this creates a 2d array).

    File.readline();                   # Throw away blank line
    character_grid  = [];              # Start off with empty character grid.

    for i in range(m):
        # First, read in the line, splitting at spaces.
        space_split_line = (File.readline()).split(" ");

        # Depending on how the file was set up, a few things can happen.
        # For one, there will be a new line character in the list. Let's get
        # rid of that.
        space_split_line = remove_newline_characters(space_split_line);

        # Next if there are multiple spaces between two characters then
        # the split method creates empty strings. Let's get rid of those first.
        space_split_line = remove_empty_elements(space_split_line);

        # Now the space split line has been processed. We're now ready to
        # add it to the character grid.
        character_grid.append(space_split_line);

    ############################################################################
    # Next, determine the number of words that we need to find.

    File.readline();                   # Throw away blank line
    k = int(File.readline());

    ############################################################################
    # Finally, read in each word, store it in the Words list.

    Words = [];

    # Loop through the words
    for i in range(k):
        # First, read in the line.
        Word = File.readline();

        # Next, remove any whitespace (tabs, newline characters, and spaces).
        Word = Word.replace(" ","");
        Word = Word.replace("\t","");
        Word = Word.replace("\n","");

        # Now that the word is processed, add it to the Words array
        Words.append(Word);

    # File has now been read, we can close the file and return our findings.
    File.close();
    return character_grid, Words;




################################################################################
# Functions to search the character grid for a particular word.

def forward_match(list, word):
    for i in range(len(word)):
        # Check if the ith letter in list matches the ith letter in word. If it
        # doesn't then we do not have a match!
        if(list[i] != word[i]):
            return False;

    # If the code makes it here then the letters of list match the corresponding
    # letters of word. This implies that we have a match!
    return True;



def backward_match(list, word):
    # Check for a forward match using the word but reversed.
    # Note: word[::-1] reverses the word.
    return forward_match(list, word[::-1]);



def search_list_for_word(list, word):
    """ This function searches for the specified word in list.
    If the word is found, then the index of the first letter of the word is
    returned. If the word is not found, -1 is returned. """

    # find the first and last letters of word as well as the word length
    first_letter = word[0];
    last_letter = word[len(word)-1];
    word_length = len(word);

    # Now, loop through the elements of list. At each point, we check if the
    # current letter matches either the first or last letter of the word.
    # If it does, then we check for a match.
    # Note: we don't need to check the final word_length letters. This is
    # because, if the word is contained in the ith row, then it can not fit
    # in the final k letters in the ith row for any k < word_length.
    last_possible_letter = len(list) - (word_length - 1);
    for i in range(last_possible_letter):
        # Check for forward match
        if(list[i] == first_letter):
            if(forward_match(list[i:i+word_length], word)):
                return i;

        # Check for backwards match
        if(list[i] == last_letter):
            if(backward_match(list[i:i+word_length], word)):
                return i+word_length;

    # If the code reaches here, then no match was found. Return -1 (indicating
    # that no match was found)
    return -1;



def search_rows_for_word(character_grid, word):
    """ This function searches for word in the rows of character_grid.
    If a word is found, then the position of the first letter of the word
    is returned. If no match is found, -1,-1 is returned. """

    # find number of rows
    m = len(character_grid);

    # Cycle through the rows of character_grid. Check for word in each one
    for i in range(m):
        ith_row = character_grid[i][:]
        j = search_list_for_word(ith_row, word);
        if(j != -1):
            return i,j;

    # if we've reached here then the word could not be found in the rows of
    # the character grid. Return -1,-1
    return -1,-1;



def search_cols_for_word(character_grid, word):
    """ This function searches for word in the columns of character_grid.
    If a word is found, then the position of the first letter of the word
    is returned. If no match is found, -1,-1 is returned. """

    # find number of columns
    n = len(character_grid[0]);

    # cycle through the columns of character_grid. Check for word in each one
    for j in range(n):
        jth_column = [row[j] for row in character_grid];
        i = search_list_for_word(jth_column, word);
        if(i != -1):
            return i,j

    # if we've reached here then the word could not be found in the columns of
    # the character grid. Return -1,-1
    return -1,-1;



def search_descending_diags_for_word(character_grid, word):
    """ This function searches for word in the descending diagionals of
    character_grid. If a word is found, then the position of the first letter
    of the word is returned. If no match is found, -1,-1 is returned. """

    # Find the number of rows and columns in character_grid. We'll need these.
    m = len(character_grid);                # num rows
    n = len(character_grid[0]);             # num cols

    # cycle through the descending diagionals of character_grid. Check for word
    # in each one. There are n+m-1 descending diagonals (think about it)
    # NOTE: k is 1 indexed (see long comment below, it makes sense to do this)
    for k in range(1,n+m+1):
        # first, we need to get the kth descending diagonal of character_grid.
        # I begin with an empty list.
        kth_diagional = [];

        """ isuppose that k < m (the number of rows). Notice that the 2nd
        descending diagional looks like
                             | - - - - - |
                             | - - - - - |
                             | # - - - - |
                             | - # - - - |
        The starting index is (2, 0), which is exactly (m-k, 0). A little thought
        reveals that this is a general result. That is, if k < m then the kth
        descending diagional starts at position (m-k,0).

        But what about when k >= m? For this, let's conisder the 6th descending
        diagonal,
                             | - - # - - |
                             | - - - # - |
                             | - - - - # |
                             | - - - - - |
        this diagional starts at position (0, 2), which is exactly (k-m, 0).
        This result is also general. If k >= m then the kth descending diagional
        starts at index (k-m, 0).

        Using these insigits, we can get the kth descending diagional. """
        # indicies of the 1st component of the kth diagonal.
        i_start = m-k if (k < m) else 0;
        j_start = 0 if (k < m) else k-m;

        # Now that we have our starting indicies, it is easy to get the kth
        # descending diagional. We simply march down and to the right until we
        # leave the grid.
        i = i_start; j = j_start;
        while(i < m and j < n):
            kth_diagional.append(character_grid[i][j]);
            i += 1;
            j += 1;

        # We now have the descending kth diagional. Let's search it for a match
        p = search_list_for_word(kth_diagional, word);
        if(p != -1):
            # the index of the pth term in the kth descending diagional is simply
            # (i_start + p, j_start +p).
            return i_start+p, j_start+p;

    # if we've reached here then the word could not be found in the descending
    # diagonals of the character grid. Return -1,-1
    return -1,-1;



def search_ascending_diags_for_word(character_grid, word):
    """ This function searches for word in the ascending diagionals of
    character_grid. If a word is found, then the position of the first letter
    of the word is returned. If no match is found, -1,-1 is returned. """

    # Find the number of rows and columns in character_grid. We'll need these.
    m = len(character_grid);                # num rows
    n = len(character_grid[0]);             # num cols

    # cycle through the ascending diagionals of character_grid. Check for word
    # in each one. There are n+m-1 ascending diagonals (think about it)
    # NOTE: k is 1-indexed (see below, it makes sense... sorta)
    for k in range(1,n+m+1):
        # first, we need to get the kth ascending diagonal of character_grid.
        # I begin with an empty list.
        kth_diagional = [];

        """ suppose that k < m (the number of rows). Notice that the 2nd
        ascending diagional looks like
                             | - # - - - |
                             | # - - - - |
                             | - - - - - |
                             | - - - - - |
        The index of the first component of this diagional is (1,0), which is
        exactly (k-1,0). A little thought reveals that this is a general result.
        If k < m then the starting index of the kth ascending diagional is (k,0).

        But what about when k >= m? For this, let's conisder the 6th ascending
        diagonal,
                             | - - - - - |
                             | - - - - # |
                             | - - - # - |
                             | - - # - - |
        this diagional starts at position (m-1, 2), which is exactly (m-1, k-m).
        This result is also general. If k >= m then the kth ascending diagional
        starts at index (m, k-m).

        Using these insigits, we can get the kth ascending diagional. """
        # indicies of the 1st component of the kth diagonal.
        i_start = k-1 if (k < m) else m-1;
        j_start = 0 if (k < m) else k-m;

        # Now that we have our starting indicies, it is easy to get the kth
        # ascending diagional. We simply march up and to the right until we leave
        # the grid.
        i = i_start; j = j_start;
        while(i >= 0 and j < n):
            kth_diagional.append(character_grid[i][j]);
            i -= 1;
            j += 1;

        # We now have the kth ascending diagional. Let's search it for a match
        p = search_list_for_word(kth_diagional, word);
        if(p != -1):
            # the index of the pth term in the kth ascending diagional is simply
            # (i_start - p, j_start +p).
            return i_start-p, j_start+p;

    # if we've reached here then the word could not be found in the ascending
    # diagonals of the character grid. Return -1,-1
    return -1,-1;



################################################################################
# Main! (the main function)

def main():
    # First, read in the character grid and words from hidden.txt
    character_grid,words = read_in_file();

    # now, determine m,n,k
    m = len(character_grid);
    n = len(character_grid[0]);
    k = len(words);


    # Cycle through the word
    for word in words:
        # Search the rows of character_grid for word
        i,j = search_rows_for_word(character_grid,word);
        if(i != -1):
            print("%s is in a row. Its first letter is at (%d, %d)"%(word, i+1,j+1));

        # Search the columns of character_grid for word
        i,j = search_cols_for_word(character_grid, word);
        if(i != -1):
            print("%s is in a column. Its first letter is at (%d, %d)"%(word, i+1,j+1));

        # Search the descending diagonals of character_grid for word.
        i,j = search_descending_diags_for_word(character_grid, word);
        if(i != -1):
            print("%s is in a descending diagonal. Its first letter is at (%d, %d)"%(word, i+1,j+1));

        # Finally, search the ascending diagionals of the character_grid for word.
        i,j = search_ascending_diags_for_word(character_grid, word);
        if(i != -1):
            print("%s is in an ascending diagonal. Its first letter is at (%d, %d)"%(word, i+1,j+1));


if(__name__ == "__main__"):
    main();
