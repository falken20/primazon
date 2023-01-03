import src


def test_get_version():
    assert src.__version__ == "1.3.0"


def test_get_name():
    assert src.__package_name__ == "primazon"
