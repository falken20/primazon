import os
from src import logger


def test_debug():
    os.environ["LEVE_LOG"] = "['DEBUG']"
    ret = logger.Log.debug("Test Debug")
    assert "Test Debug" in ret


def test_debug_no_trace():
    os.environ["LEVE_LOG"] = "[]"
    ret = logger.Log.debug("Test debug") 
    assert ret is None

