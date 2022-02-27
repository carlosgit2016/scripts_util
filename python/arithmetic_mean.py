from functools import reduce
from pprint import pprint

def arithmetic_mean(d, n):
    sum = 0
    for i in range(n):
        sum += d[i]
    
    return sum / n

def test_arithmetic_mean():
    expected_arithmetic_mean_results = [
        {
            'number_of_values': 4,
            'data_set_values': [89,90,100,900],
            'arithmetic_mean': 294.75
        },
        {
            'number_of_values': 2,
            'data_set_values': [70, 65],
            'arithmetic_mean': 67.5
        }
    ]

    for expected_arithmetic_mean in expected_arithmetic_mean_results:
        arithmetic_mean_result = arithmetic_mean(expected_arithmetic_mean['data_set_values'], expected_arithmetic_mean['number_of_values'])
        assert arithmetic_mean_result == expected_arithmetic_mean['arithmetic_mean']

def weighted_arithmetic_mean(d, w, n):
    sum_of_weight = reduce(lambda w1, w2: w1 + w2, w)
    sum_of_values = 0
    for i in range(n):
        sum_of_values += w[i]*d[i]
    weighted_arithmetic_mean_result = sum_of_values / sum_of_weight
    # Rounding the result 
    # It is a process that returns the closest finite number expressed to two decimal places
    return round(weighted_arithmetic_mean_result, 4)

def test_weighted_arithmetic_mean():
    expected_weighted_arithmetic_mean_results = [
        {
            'number_of_terms': 2,
            'values': [89, 11],
            'weights_to_values': [70, 30],
            'weighted_average': 65.6
        },
        {
            'number_of_terms': 6,
            'values': [3, 8, 10, 17, 24, 27],
            'weights_to_values': [2, 8, 10, 13, 18, 20],
            'weighted_average': 19.1972
        },
        {
            'number_of_terms': 10,
            'values': [10, 9, 2, 1, 8, 7, 3, 6, 5, 4],
            'weights_to_values': [2, 8, 10, 13, 18, 20, 5, 9, 3, 11],
            'weighted_average': 5.4242
        },

    ]

    for expected_weighted_arithmetic_mean in expected_weighted_arithmetic_mean_results:
        weighted_arithmetic_result = weighted_arithmetic_mean(expected_weighted_arithmetic_mean['values'], expected_weighted_arithmetic_mean['weights_to_values'], expected_weighted_arithmetic_mean['number_of_terms'])
        assert weighted_arithmetic_result == expected_weighted_arithmetic_mean['weighted_average']