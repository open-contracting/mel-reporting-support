import pytest

from ocdskit.cli.__main__ import main
from tests import assert_stdout, path, assert_stdout_error


def test_command(monkeypatch):
    assert_stdout(monkeypatch, main,
                  ['mapping-sheet', '--infer-required', path('release-schema.json')],
                  'mapping-sheet.csv')


def test_command_order_by(monkeypatch):
    assert_stdout(monkeypatch, main,
                  ['mapping-sheet', '--infer-required', '--order-by', 'path', path('release-schema.json')],
                  'mapping-sheet_order-by.csv')


@pytest.mark.vcr()
def test_command_extension(monkeypatch):
    url = 'https://github.com/open-contracting-extensions/ocds_lots_extension/archive/master.zip'

    assert_stdout(monkeypatch, main,
                  ['mapping-sheet', '--infer-required', path('release-schema.json'), '--extension', url],
                  'mapping-sheet_extension.csv')


def test_command_extension_field(monkeypatch):
    assert_stdout(monkeypatch, main,
                  ['mapping-sheet', '--infer-required', '--extension-field', 'extension',
                   path('release-schema-patched.json')],
                  'mapping-sheet_extension-field.csv')


@pytest.mark.vcr()
def test_command_extension_and_extension_field(monkeypatch):
    url = 'https://github.com/open-contracting-extensions/ocds_lots_extension/archive/master.zip'

    assert_stdout(monkeypatch, main,
                  ['mapping-sheet', '--infer-required', '--extension-field', 'extension',
                   path('release-schema.json'), '--extension', url],
                  'mapping-sheet_extension-field.csv')


def test_command_oc4ids(monkeypatch):
    assert_stdout(monkeypatch, main,
                  ['mapping-sheet', path('project-schema.json')],
                  'mapping-sheet_oc4ids.csv')


def test_command_bods(monkeypatch):
    assert_stdout(monkeypatch, main,
                  ['mapping-sheet', '--order-by', 'path', path('bods/person-statement.json')],
                  'mapping-sheet_bods.csv')


def test_command_sedl(monkeypatch):
    assert_stdout(monkeypatch, main,
                  ['mapping-sheet', path('sedl-schema.json')],
                  'mapping-sheet_sedl.csv')


def test_command_order_by_nonexistent(monkeypatch, caplog):
    assert_stdout_error(monkeypatch, main, ['mapping-sheet', '--order-by', 'nonexistent', path('release-schema.json')])

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'CRITICAL'
    assert caplog.records[0].message == "the column 'nonexistent' doesn't exist – did you make a typo?"
