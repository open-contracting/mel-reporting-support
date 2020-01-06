import json
from tempfile import TemporaryFile

import pytest

from ocdskit.util import is_record, json_dump
from tests import read


# Same fixture files as in test_detect_format.py, except for concatenated JSON files.
@pytest.mark.parametrize('filename,expected', [
    ('record-package_minimal.json', False),
    ('release-package_minimal.json', False),
    ('record_minimal.json', True),
    ('release_minimal.json', False),
    ('realdata/compiled-release-1.json', False),
    ('realdata/versioned-release-1.json', False),
    ('release-packages.json', False),
    ('detect-format_whitespace.json', False),
])
def test_is_record(filename, expected):
    assert is_record(json.loads(read(filename))) == expected


@pytest.mark.parametrize('data,expected', [
    (iter([]), '[]'),
    ({'a': 1, 'b': 2}, '{"a":1,"b":2}'),
])
def test_json_dump(data, expected):
    with TemporaryFile('w+') as f:
        json_dump(data, f)

        f.seek(0)

        assert f.read() == expected