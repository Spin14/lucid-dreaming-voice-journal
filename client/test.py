from unittest.mock import patch

def ola():
    print("ola")

def mock_ola():
    print("mocked ola")

def call_ola():
    ola()

@patch('test.ola', side_effect = mock_ola)
def try_mock(m):

    call_ola()

if __name__ == '__main__':
    print('--')
    call_ola()
    print('--')
    try_mock()
    print('--')