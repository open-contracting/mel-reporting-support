import sys
from io import BytesIO, StringIO, TextIOWrapper
from unittest.mock import patch

from ocdskit.cli.__main__ import main

# Taken from test_set_closed_codelist_enums.py
stdin = b'''{
  "properties": {
    "closedStringNull": {
      "type": [
        "string",
        "null"
      ],
      "codelist": "a.csv",
      "openCodelist": false
    },
    "closedArrayNull": {
      "type": [
        "array",
        "null"
      ],
      "codelist": "b.csv",
      "openCodelist": false,
      "items": {
        "type": "string"
      }
    },
    "closedString": {
      "type": "string",
      "codelist": "c.csv",
      "openCodelist": false
    },
    "closedDisorder": {
      "type": "string",
      "codelist": "d.csv",
      "openCodelist": false,
      "enum": [
        "bar",
        "foo"
      ]
    },
    "open": {
      "type": [
        "string",
        "null"
      ],
      "codelist": "a.csv",
      "openCodelist": true
    }
  }
}
'''


def test_command(monkeypatch):
    with patch('sys.stdin', TextIOWrapper(BytesIO(stdin))), patch('sys.stdout', new_callable=StringIO) as actual:
        monkeypatch.setattr(sys, 'argv', ['ocdskit', 'schema-report', '--min-occurrences', '2'])
        main()

    assert actual.getvalue() == '''codelist,openness
a.csv,closed/open
b.csv,closed
c.csv,closed
d.csv,closed

 2: {'type': ['string', 'null']}
 2: {'type': 'string'}
'''


def test_command_no_codelists(monkeypatch):
    with patch('sys.stdin', TextIOWrapper(BytesIO(stdin))), patch('sys.stdout', new_callable=StringIO) as actual:
        monkeypatch.setattr(sys, 'argv', ['ocdskit', 'schema-report', '--min-occurrences', '2', '--no-codelists'])
        main()

    assert 'codelist' not in actual.getvalue()


def test_command_no_definitions(monkeypatch):
    with patch('sys.stdin', TextIOWrapper(BytesIO(stdin))), patch('sys.stdout', new_callable=StringIO) as actual:
        monkeypatch.setattr(sys, 'argv', ['ocdskit', 'schema-report', '--min-occurrences', '2', '--no-definitions'])
        main()

    assert ':' not in actual.getvalue()


def test_command_min_occurrences(monkeypatch):
    with patch('sys.stdin', TextIOWrapper(BytesIO(stdin))), patch('sys.stdout', new_callable=StringIO) as actual:
        monkeypatch.setattr(sys, 'argv', ['ocdskit', 'schema-report', '--min-occurrences', '1', '--no-codelists'])
        main()

    assert '1:' in actual.getvalue()
