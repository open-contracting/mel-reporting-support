from .base import BaseCommand
from ocdskit.combine import combine_release_packages


class Command(BaseCommand):
    name = 'combine-release-packages'
    help = 'reads release packages from standard input, collects releases, and prints one release package'

    def add_arguments(self):
        self.add_package_arguments('release')

    def handle(self):
        kwargs = self.parse_package_arguments()

        output = combine_release_packages(self.buffer(), **kwargs)

        self.print(output)
