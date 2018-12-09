# test structure.py for expected output 
# inputs in inputs.txt

# outputs

import structure
good = "Perhaps correct - no error found for format"
bad = ""
short = ""

def test_are_equal(actual, expected):
    assert expected == actual, "Expected {0}, got {1}".format(expected, actual)
    
def test_not_equal(a, e):
    assert a != e, "Did not expect {0} but got {1}".format(a, e)
    
def test_good_phrases(list):
    expected = good
    for i in range[1,4]:
        actual = structure.main(i,"stat","test")     #main(line, sq, cc)
        test_are_equal(actual, expected)
    print("All tests passed!")   

    
    