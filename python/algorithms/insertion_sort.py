def asc_insertion_sort(sequence_of_numbers):
    sequence_of_numbers_copy = sequence_of_numbers.copy()

    for j in range(1, len(sequence_of_numbers_copy), 1):
        key = sequence_of_numbers_copy[j]
        i = j - 1
        while i > -1 and sequence_of_numbers_copy[i] > key:
            sequence_of_numbers_copy[i+1] = sequence_of_numbers_copy[i]
            i = i - 1
        sequence_of_numbers_copy[i+1] = key

    return sequence_of_numbers_copy

def test_asc_insertion_sort():

    expected_results = [
        {
            'sequence': [1, 5, 2, 3, 4]
        },
        {
            'sequence': [1, 3, 6, 5, 2, 7, 4, 10, 8, 9]
        },
        {
            'sequence': [22, 9, 14, 45, 43, 29, 48, 8, 41, 46, 36, 24, 10, 33, 2, 23, 3, 47, 39, 35, 18, 28, 31, 16, 30, 19, 32, 6, 13, 21, 11, 7, 44, 5, 26, 42, 50, 27, 1, 49, 37, 17, 15, 38, 20, 25, 34, 40, 12, 4]
        },
        {
            'sequence': [5, 2, 4, 6, 1, 3]
        }
    ]
    
    for expected_result in expected_results:
        expected_result_sorted = expected_result['sequence'].copy()
        expected_result_sorted.sort()
        assert expected_result_sorted == asc_insertion_sort(expected_result['sequence'])


if __name__ == "__main__":
    print(asc_insertion_sort([5, 2, 4, 6, 1, 3]))