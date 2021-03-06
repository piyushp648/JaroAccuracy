import os
from math import floor
import re
'''
Add all the actual output in .\\actual folder
all the observed output in .\\oberved folder
run the program, you'll find accuracy calculated in accuracy.txt
'''

# Function to calculate the
# Jaro Similarity of two strings


def jaro_distance(s1, s2):

    # If the s are equal
    if (s1 == s2):
        return 1.0

    # Length of two s
    len1 = len(s1)
    len2 = len(s2)

    # Maximum distance upto which matching
    # is allowed
    max_dist = floor(max(len1, len2) / 2) - 1

    # Count of matches
    match = 0

    # Hash for matches
    hash_s1 = [0] * len(s1)
    hash_s2 = [0] * len(s2)

    # Traverse throgh the first
    for i in range(len1):

        # Check if there is any matches
        for j in range(max(0, i - max_dist), min(len2, i + max_dist + 1)):

            # If there is a match
            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break

    # If there is no match
    if (match == 0):
        return 0.0

    # Number of transpositions
    t = 0
    point = 0

    # Count number of occurances
    # where two characters match but
    # there is a third matched character
    # in between the indices
    for i in range(len1):
        if (hash_s1[i]):

            # Find the next matched character
            # in second
            while (hash_s2[point] == 0):
                point += 1

            if (s1[i] != s2[point]):
                point += 1
                t += 1
    t = t//2

    # Return the Jaro Similarity
    return (match / len1 + match / len2 +
            (match - t + 1) / match) / 3.0


def jaro_winkler_distance(s1, s2):

    # If the strings are equal
    if (s1 == s2):
        return 1.0

    # Length of two strings
    len1 = len(s1)
    len2 = len(s2)

    if (len1 == 0 or len2 == 0):
        return 0.0

    # Maximum distance upto which matching
    # is allowed
    max_dist = (max(len(s1), len(s2)) // 2) - 1

    # Count of matches
    match = 0

    # Hash for matches
    hash_s1 = [0] * len(s1)
    hash_s2 = [0] * len(s2)

    # Traverse throgh the first string
    for i in range(len1):

        # Check if there is any matches
        for j in range(max(0, i - max_dist), min(len2, i + max_dist + 1)):

            # If there is a match
            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break

    # If there is no match
    if (match == 0):
        return 0.0

    # Number of transpositions
    t = 0

    point = 0

    # Count number of occurances
    # where two characters match but
    # there is a third matched character
    # in between the indices
    for i in range(len1):
        if (hash_s1[i]):

            # Find the next matched character
            # in second string
            while (hash_s2[point] == 0):
                point += 1

            if (s1[i] != s2[point]):
                point += 1
                t += 1
            else:
                point += 1

        t /= 2

    # Return the Jaro Similarity
    return ((match / len1 + match / len2 + (match - t) / match) / 3.0)

# Jaro Winkler Similarity


def jaro_Winkler(s1, s2):

    jaro_dist = jaro_distance(s1, s2)

    # If the jaro Similarity is above a threshold
    if (jaro_dist > 0.7):

        # Find the length of common prefix
        prefix = 0

        for i in range(min(len(s1), len(s2))):

            # If the characters match
            if (s1[i] == s2[i]):
                prefix += 1

            # Else break
            else:
                break

        # Maximum of 4 characters are allowed in prefix
        prefix = min(4, prefix)

        # Calculate jaro winkler Similarity
        jaro_dist += 0.1 * prefix * (1 - jaro_dist)

    return jaro_dist


# Driver code
if __name__ == "__main__":

    # s1 = open("36_actual.txt").read().replace('\n', ' ').replace('\r', '')
    # s2 = open("36_output.txt").read().replace('\n', ' ').replace('\r', '')

    # num_files = 2

    files = os.listdir(".\\observed\\")
    # getting list of files from actual dir only since
    # there's a file in observed corresponding to each file
    # in actual directory
    # accuracy = dict()
    sum = 0
    output_file = open("accuracy.txt", "w+")
    i = 1
    for file in files:
        if not file.endswith(".txt"):
            continue
        file1 = ".\\actual\\" + file
        file2 = ".\\observed\\" + file
        try:
            s1 = open(file1, encoding="utf-8").read().replace('\n', ' ').replace('\r', '')
            s2 = open(file2, encoding="utf-8").read().replace('\n', ' ').replace('\r', '')
        except IOError:
            print(f'File {file} does not exist in one of the folders')
            continue
        s1 = re.sub(r'[^\x00-\x7F]+', ' ', s1)
        s2 = re.sub(r'[^\x00-\x7F]+', ' ', s2)

        accuracy = jaro_Winkler(s1, s2)
        sum += accuracy
        output_file.write(str(i) + ". " + file.split('.')[0] + " : " + str("{:.4f}".format(accuracy)) + "\n")
        i += 1

    output_file.write(f'Mean Accuracy = {sum/i}')
    output_file.close()

    # for item in accuracy:
    #     output_file.write(str(item) + "\n")
    # Print Jaro-Winkler Similarity of two strings


# This code is contributed by AnkitRai01
