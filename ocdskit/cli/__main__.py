import argparse
import importlib
import logging
import sys

import ijson

from ocdskit.exceptions import CommandError

logger = logging.getLogger('ocdskit')

COMMAND_MODULES = (
    'ocdskit.cli.commands.combine_record_packages',
    'ocdskit.cli.commands.combine_release_packages',
    'ocdskit.cli.commands.compile',
    'ocdskit.cli.commands.detect_format',
    'ocdskit.cli.commands.echo',
    'ocdskit.cli.commands.indent',
    'ocdskit.cli.commands.mapping_sheet',
    'ocdskit.cli.commands.package_records',
    'ocdskit.cli.commands.package_releases',
    'ocdskit.cli.commands.schema_report',
    'ocdskit.cli.commands.schema_strict',
    'ocdskit.cli.commands.set_closed_codelist_enums',
    'ocdskit.cli.commands.split_record_packages',
    'ocdskit.cli.commands.split_release_packages',
    'ocdskit.cli.commands.tabulate',
    'ocdskit.cli.commands.upgrade',
    'ocdskit.cli.commands.validate',
)


def main():
    parser = argparse.ArgumentParser(description='Open Contracting Data Standard CLI')
    parser.add_argument('--encoding', help='the file encoding')
    parser.add_argument('--ascii', help='print escape sequences instead of UTF-8 characters', action='store_true')
    parser.add_argument('--pretty', help='pretty print output', action='store_true')

    subparsers = parser.add_subparsers(dest='subcommand')

    subcommands = {}

    for module in COMMAND_MODULES:
        try:
            command = importlib.import_module(module).Command(subparsers)
            subcommands[command.name] = command
        except ImportError as e:
            logger.error('exception "%s" prevented loading of %s module', e, module)

    args = parser.parse_args()

    if args.subcommand:
        command = subcommands[args.subcommand]
        try:
            command.args = args
            try:
                command.handle()
            except ijson.common.IncompleteJSONError as e:
                if str(e):
                    raise CommandError('JSON error: {}'.format(e))
                _raise_encoding_error(e, args.encoding)
            except UnicodeDecodeError as e:
                _raise_encoding_error(e, args.encoding)
        except CommandError as e:
            logger.critical(e)
            sys.exit(1)
    else:
        parser.print_help()


def _raise_encoding_error(e, encoding):
    if encoding and encoding.lower() == 'iso-8859-1':
        suggestion = 'utf-8'
    else:
        suggestion = 'iso-8859-1'
    raise CommandError('encoding error: {}\nTry `--encoding {}`?'.format(e, suggestion))


if __name__ == '__main__':
    main()
