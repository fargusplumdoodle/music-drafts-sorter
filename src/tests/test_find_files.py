from src.find_files import is_supported


def test_is_supported_wav():
    assert is_supported("asdf.wav")
    assert not is_supported("asdfwav")


def test_is_supported_mp3():
    assert is_supported("asdf.mp3")
    assert not is_supported("asdfmp3")


def test_is_supported_m4a():
    assert is_supported("asdf.m4a")
    assert not is_supported("asdfm4a")
