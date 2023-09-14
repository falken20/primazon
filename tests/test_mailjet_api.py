import src.mailjet_api as mj_api


def test_mailjet_vars():
    assert mj_api.api_key is not None
    assert mj_api.api_secret is not None
    assert mj_api.api_version is not None
    assert mj_api.receiver_email is not None
    assert mj_api.text_part_default is not None
    assert mj_api.data is not None


def test_mailjet_api():
    result = mj_api.send_email(text_part="Testing sending mail")
    assert result is True
