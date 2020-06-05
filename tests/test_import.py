def test_import():
    import brukeropusreader as bor
    l = dir(bor)
    assert 'opus_reader' in l

