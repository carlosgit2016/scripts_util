from extract_value import normalize

def test_normalize():
    input = "R$ 27,46"
    expected = 27.46

    assert normalize(input) == expected