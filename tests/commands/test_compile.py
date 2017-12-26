import sys
from io import BytesIO, StringIO, TextIOWrapper
from unittest.mock import patch

import pytest

from ocdskit.cli.__main__ import main
from tests import read


def test_command(monkeypatch):
    stdin = read('realdata/release-package-1.json', 'rb') + read('realdata/release-package-2.json', 'rb')

    with patch('sys.stdin', TextIOWrapper(BytesIO(stdin))), patch('sys.stdout', new_callable=StringIO) as actual:
        monkeypatch.setattr(sys, 'argv', ['ocdskit', 'compile'])
        main()

    assert actual.getvalue() == read('realdata/compiled-release-1.json') + read('realdata/compiled-release-2.json')


def test_command_help(monkeypatch, caplog):
    stdin = read('release-package_minimal.json', 'rb')

    with pytest.raises(SystemExit) as excinfo:
        with patch('sys.stdin', TextIOWrapper(BytesIO(stdin))), patch('sys.stdout', new_callable=StringIO) as actual:
            monkeypatch.setattr(sys, 'argv', ['ocdskit', '--help'])
            main()

    assert len(caplog.records()) == 0
    assert excinfo.value.code == 0

    assert actual.getvalue().startswith('usage: ocdskit [-h] ')


def test_command_pretty(monkeypatch):
    stdin = read('release-package_minimal.json', 'rb')

    with patch('sys.stdin', TextIOWrapper(BytesIO(stdin))), patch('sys.stdout', new_callable=StringIO) as actual:
        monkeypatch.setattr(sys, 'argv', ['ocdskit', '--pretty', 'compile'])
        main()

    assert actual.getvalue() == read('compile_pretty_minimal.json')


def test_command_encoding(monkeypatch, caplog):
    stdin = read('realdata/release-package_encoding-iso-8859-1.json', 'rb')

    with patch('sys.stdin', TextIOWrapper(BytesIO(stdin))), patch('sys.stdout', new_callable=StringIO) as actual:
        monkeypatch.setattr(sys, 'argv', ['ocdskit', '--encoding', 'iso-8859-1', 'compile'])
        main()

    assert actual.getvalue() == read('realdata/compile_encoding_encoding.json')


def test_command_bad_encoding_iso_8859_1(monkeypatch, caplog):
    stdin = read('realdata/release-package_encoding-iso-8859-1.json', 'rb')

    with pytest.raises(SystemExit) as excinfo:
        with patch('sys.stdin', TextIOWrapper(BytesIO(stdin))), patch('sys.stdout', new_callable=StringIO):
            monkeypatch.setattr(sys, 'argv', ['ocdskit', 'compile'])
            main()

    assert len(caplog.records()) == 1
    assert caplog.records()[0].levelname == 'CRITICAL'
    assert caplog.records()[0].message == "encoding error: try `--encoding iso-8859-1`? ('utf-8' codec can't decode " \
                                          "byte 0xd3 in position 592: invalid continuation byte)"
    assert excinfo.value.code == 1