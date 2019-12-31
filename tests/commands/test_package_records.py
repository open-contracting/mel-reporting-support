from ocdskit.cli.__main__ import main
from tests import assert_streaming


def test_command(monkeypatch):
    assert_streaming(monkeypatch, main, ['package-records', '--uri', 'http://example.com', '--published-date',
                                         '9999-01-01T00:00:00Z', '--publisher-name', ''],
                     ['record_minimal-1.json', 'record_minimal-2.json'],
                     ['record-package_minimal-1-2.json'])


def test_command_extensions(monkeypatch):
    assert_streaming(monkeypatch, main, ['package-records', '--uri', 'http://example.com', '--published-date',
                                         '9999-01-01T00:00:00Z', '--publisher-name', '',
                                         'http://example.com/a/extension.json', 'http://example.com/b/extension.json'],
                     ['record_minimal-1.json', 'record_minimal-2.json'],
                     ['record-package_minimal-1-2-extensions.json'])


def test_command_root_path_array(monkeypatch):
    assert_streaming(monkeypatch, main, ['package-records', '--root-path', 'records'],
                     ['realdata/record-package-1.json', 'realdata/record-package-2.json'],
                     ['realdata/record-package_record-package.json'])


def test_command_root_path_item(monkeypatch):
    assert_streaming(monkeypatch, main, ['package-records', '--root-path', 'records.item'],
                     ['realdata/record-package-1.json', 'realdata/record-package-2.json'],
                     ['realdata/record-package_record-package.json'])
