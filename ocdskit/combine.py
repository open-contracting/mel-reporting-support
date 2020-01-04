from ocdsextensionregistry import ProfileBuilder
from ocdsmerge import Merger
from ocdsmerge.util import get_release_schema_url, get_tags

from ocdskit.packager import Packager
from ocdskit.util import (_empty_record_package, _empty_release_package, _remove_empty_optional_metadata,
                          _resolve_metadata, _update_package_metadata)


def _package(key, items, uri, publisher, published_date, extensions):
    if publisher is None:
        publisher = {}
    if 'name' not in publisher:
        publisher['name'] = ''
    if extensions is None:
        extensions = []

    output = {
        'uri': uri,
        'publisher': publisher,
        'publishedDate': published_date,
        'version': '1.1',  # fields might be deprecated
        'extensions': extensions,
        key: items,
    }

    return output


def package_records(records, uri='', publisher=None, published_date='', extensions=None):
    """
    Wraps records in a record package.

    :param list records: a list of records
    :param str uri: the record package's ``uri``
    :param dict publisher: the record package's ``publisher``
    :param str published_date: the record package's ``publishedDate``
    :param list extensions: the record package's ``extensions``
    """
    return _package('records', records, uri, publisher, published_date, extensions)


def package_releases(releases, uri='', publisher=None, published_date='', extensions=None):
    """
    Wraps releases in a release package.

    :param list releases: a list of releases
    :param str uri: the release package's ``uri``
    :param dict publisher: the release package's ``publisher``
    :param str published_date: the release package's ``publishedDate``
    :param list extensions: the release package's ``extensions``
    """
    return _package('releases', releases, uri, publisher, published_date, extensions)


def combine_record_packages(packages, uri='', publisher=None, published_date=''):
    """
    Collects the packages and records from the record packages into one record package.

    :param packages: an iterable of record packages
    :param str uri: the record package's ``uri``
    :param dict publisher: the record package's ``publisher``
    :param str published_date: the record package's ``publishedDate``
    """
    # See options for not buffering all inputs into memory: https://github.com/open-contracting/ocdskit/issues/119
    output = _empty_record_package(uri, publisher, published_date)
    output['packages'] = {}

    for package in packages:
        _update_package_metadata(output, package)
        output['records'].extend(package['records'])
        if 'packages' in package:
            output['packages'].update(dict.fromkeys(package['packages']))

    if publisher:
        output['publisher'] = publisher

    _resolve_metadata(output, 'packages')
    _resolve_metadata(output, 'extensions')
    _remove_empty_optional_metadata(output)

    return output


def combine_release_packages(packages, uri='', publisher=None, published_date=''):
    """
    Collects the releases from the release packages into one release package.

    :param packages: an iterable of release packages
    :param str uri: the release package's ``uri``
    :param dict publisher: the release package's ``publisher``
    :param str published_date: the release package's ``publishedDate``
    """
    # See options for not buffering all inputs into memory: https://github.com/open-contracting/ocdskit/issues/119
    output = _empty_release_package(uri, publisher, published_date)

    for package in packages:
        _update_package_metadata(output, package)
        output['releases'].extend(package['releases'])

    if publisher:
        output['publisher'] = publisher

    _resolve_metadata(output, 'extensions')
    _remove_empty_optional_metadata(output)

    return output


def merge(data, uri='', publisher=None, published_date='', schema=None, return_versioned_release=False,
          return_package=False, use_linked_releases=False, streaming=False):
    """
    Merges release packages and individual releases.

    By default, yields compiled releases. If ``return_versioned_release`` is ``True``, yields versioned releases. If
    ``return_package`` is ``True``, wraps the compiled releases (and versioned releases if ``return_versioned_release``
    is ``True``) in a record package.

    If ``return_package`` is set and ``publisher`` isn't set, the output record package will have the same publisher as
    the last input release package.

    :param data: an iterable of release packages and individual releases
    :param str uri: if ``return_package`` is ``True``, the record package's ``uri``
    :param dict publisher: if ``return_package`` is ``True``, the record package's ``publisher``
    :param str published_date: if ``return_package`` is ``True``, the record package's ``publishedDate``
    :param dict schema: the URL, path or dict of the patched release schema to use
    :param bool return_package: wrap the compiled releases in a record package
    :param bool use_linked_releases: if ``return_package`` is ``True``, use linked releases instead of full releases,
        if the input is a release package
    :param bool return_versioned_release: if ``return_package`` is ``True``, include versioned releases in the record
        package; otherwise, yield versioned releases instead of compiled releases
    :param bool streaming: if ``return_package`` is ``True``, set the package's records to a generator (this only works
        if the calling code exhausts the generator before ``merge`` returns)
    """
    with Packager() as packager:
        packager.add(data)

        if not schema and packager.version:
            prefix = packager.version.replace('.', '__') + '__'
            tag = next(tag for tag in reversed(get_tags()) if tag.startswith(prefix))
            schema = get_release_schema_url(tag)

            if packager.package['extensions']:
                builder = ProfileBuilder(tag, list(packager.package['extensions']))
                schema = builder.patched_release_schema()

        merger = Merger(schema)

        if return_package:
            packager.package['uri'] = uri
            packager.package['publishedDate'] = published_date
            if publisher:
                packager.package['publisher'] = publisher

            yield from packager.output_package(merger, return_versioned_release=return_versioned_release,
                                               use_linked_releases=use_linked_releases, streaming=streaming)
        else:
            yield from packager.output_releases(merger, return_versioned_release=return_versioned_release)
