from page_loader import download
import pytest

test_cases = ['1']


@pytest.mark.parametrize('test', test_cases)
def test_main(test):
    print(test)
    assert download() == 'start'
