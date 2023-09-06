import src.mail_config as mc


def test_content_vars():
    assert mc.smtp_server is not None
    assert mc.sender_email is not None
    assert mc.receiver_email is not None
    assert mc.message is not None
    assert mc.message_plaintext is not None
    assert mc.message_html is not None
