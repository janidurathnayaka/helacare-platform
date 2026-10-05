from app.scripts.import_plants import is_verified


def test_unverified_status_is_false():
    assert is_verified("UNVERIFIED") is False


def test_source_verified_status_is_true():
    assert is_verified("Source-verified ethnobotanical record") is True


def test_approved_status_is_true():
    assert is_verified("approved") is True
