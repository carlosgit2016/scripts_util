def percentual_discount(v, p):
    return (v/100) * p

def test_percentual_discount():
    expected_results = [
        {
            'value': 500,
            'percentual_discount': 10,
            'result': 50
        },
        {
            'value': 24897362,
            'percentual_discount': 20,
            'result': 4979472.4
        }
    ]

    for expected_result in expected_results:
        result = percentual_discount(expected_result['value'], expected_result['percentual_discount'])
        assert expected_result['result'] == result