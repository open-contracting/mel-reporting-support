OCDS Commands
=============

Optional arguments for all commands are:

* ``--encoding ENCODING`` the file encoding
* ``--pretty`` pretty print output

compile
-------

Reads release packages from standard input, merges the releases by OCID, and prints the compiled releases.

If ``--package`` is set, and if the ``--publisher-*`` options aren't used, the output package will have the same publisher as the last input package.

Optional arguments:

* ``--schema SCHEMA`` the URL or path of the release schema to use
* ``--package`` wrap the compiled releases in a record package
* ``--linked-releases`` if ``--package`` is set, use linked releases instead of full releases
* ``--versioned`` if ``--package`` is set, include versioned releases in the record package; otherwise, print versioned releases instead of compiled releases
* ``--uri URI`` if ``--package`` is set, set the record package's ``uri`` to this value
* ``--published-date PUBLISHED_DATE`` if ``--package`` is set, set the record package's ``publishedDate`` to this value
* ``--publisher-name PUBLISHER_NAME`` set the record package's ``publisher``'s ``name`` to this value
* ``--publisher-uri PUBLISHER_URI`` set the record package's ``publisher``'s ``uri`` to this value
* ``--publisher-scheme PUBLISHER_SCHEME`` set the record package's ``publisher``'s ``scheme`` to this value
* ``--publisher-uid PUBLISHER_UID`` set the record package's ``publisher``'s ``uid`` to this value

::

    cat tests/fixtures/realdata/release-package-1.json | ocdskit compile > out.json

upgrade
-------

Upgrades packages and releases from an old version of OCDS to a new version. Any data not in the old version is passed through. **Note:** Versioned releases within a record package are not upgraded.

OCDS 1.0 `describes <https://standard.open-contracting.org/1.0/en/schema/reference/#identifier>`__ an organization's ``name``, ``identifier``, ``address`` and ``contactPoint`` as relevant to identifying it. OCDS 1.1 `moves <https://standard.open-contracting.org/1.1/en/schema/reference/#parties>`__ organization data into a ``parties`` array. To upgrade from OCDS 1.0 to 1.1, we create an ``id`` for each organization, based on those identifying fields. This can result in duplicates in the ``parties`` array, if the same organization has different or missing values for identifying fields in different contexts. This can also lead to data loss if the same organization has different values for non-identifying fields in different contexts; the command prints warnings in such cases.

**Note:** OCDS 1.0 uses the `whole-list merge <https://standard.open-contracting.org/1.0/en/schema/merging/#merging-rules>`__ strategy on the `suppliers` array to prepare the compiled release and versioned release, whereas OCDS 1.1 uses the `identifier merge <https://standard.open-contracting.org/1.1/en/schema/merging/#identifier-merge>`__ strategy. This means that you should merge first and then upgrade.

::

    cat tests/fixtures/realdata/release-package-1.json | ocdskit upgrade 1.0:1.1 > out.json

package-releases
----------------

Reads releases from standard input, and prints one release package.

Optional positional arguments:

* ``extension`` add this extension to the package
* ``--uri URL`` set the release package's ``uri`` to this value
* ``--published-date PUBLISHED_DATE`` set the release package's ``publishedDate`` to this value
* ``--publisher-name PUBLISHER_NAME`` set the release package's ``publisher``'s ``name`` to this value
* ``--publisher-uri PUBLISHER_URI`` set the release package's ``publisher``'s ``uri`` to this value
* ``--publisher-scheme PUBLISHER_SCHEME`` set the release package's ``publisher``'s ``scheme`` to this value
* ``--publisher-uid PUBLISHER_UID`` set the release package's ``publisher``'s ``uid`` to this value

::

    cat tests/fixtures/release_*.json | ocdskit package-releases > out.json

To convert record packages to a release package, you can use `use jq <https://github.com/open-contracting/ocdskit/blob/master/docs/Using_jq.md>`__ to get the releases from the record packages, along with the ``package-releases`` command.

::

    cat tests/fixtures/realdata/record-package* | jq -crM .records[].releases[] | ocdskit package-releases

combine-record-packages
-----------------------

Reads record packages from standard input, collects packages and records, and prints one record package.

If the ``--publisher-*`` options aren't used, the output package will have the same publisher as the last input package.

Optional arguments:

* ``--uri URL`` set the record package's ``uri`` to this value
* ``--published-date PUBLISHED_DATE`` set the record package's ``publishedDate`` to this value
* ``--publisher-name PUBLISHER_NAME`` set the record package's ``publisher``'s ``name`` to this value
* ``--publisher-uri PUBLISHER_URI`` set the record package's ``publisher``'s ``uri`` to this value
* ``--publisher-scheme PUBLISHER_SCHEME`` set the record package's ``publisher``'s ``scheme`` to this value
* ``--publisher-uid PUBLISHER_UID`` set the record package's ``publisher``'s ``uid`` to this value

::

    cat tests/fixtures/record-package_*.json | ocdskit combine-record-packages > out.json

combine-release-packages
------------------------

Reads release packages from standard input, collects releases, and prints one release package.

If the ``--publisher-*`` options aren't used, the output package will have the same publisher as the last input package.

Optional arguments:

* ``--uri URL`` set the release package's ``uri`` to this value
* ``--published-date PUBLISHED_DATE`` set the release package's ``publishedDate`` to this value
* ``--publisher-name PUBLISHER_NAME`` set the release package's ``publisher``'s ``name`` to this value
* ``--publisher-uri PUBLISHER_URI`` set the release package's ``publisher``'s ``uri`` to this value
* ``--publisher-scheme PUBLISHER_SCHEME`` set the release package's ``publisher``'s ``scheme`` to this value
* ``--publisher-uid PUBLISHER_UID`` set the release package's ``publisher``'s ``uid`` to this value

::

    cat tests/fixtures/release-package_*.json | ocdskit combine-release-packages > out.json

split-record-packages
---------------------

Reads record packages from standard input, and prints smaller record packages for each.

::

    cat tests/fixtures/realdata/record-package-1.json | ocdskit split-record-packages 2 | split -l 1 -a 4

The ``split`` command will write files named ``xaaaa``, ``xaaab``, ``xaaac``, etc. Don't combine the OCDS Kit ``--pretty`` option with the ``split`` command.

split-release-packages
----------------------

Reads release packages from standard input, and prints smaller release packages for each.

::

    cat tests/fixtures/realdata/release-package-1.json | ocdskit split-release-packages 2 | split -l 1 -a 4

The ``split`` command will write files named ``xaaaa``, ``xaaab``, ``xaaac``, etc. Don't combine the OCDS Kit ``--pretty`` option with the ``split`` command.

tabulate
--------

Load packages into a database.

Optional arguments:

* ``--drop`` drop all tables before loading
* ``--schema SCHEMA`` the release-schema.json to use

::

    cat release_package.json | ocdskit tabulate sqlite:///data.db

For the format of ``database_url``, see the `SQLAlchemy documentation <https://docs.sqlalchemy.org/en/rel_1_1/core/engines.html#database-urls>`__.

validate
--------

Reads JSON data from standard input, validates it against the schema, and prints errors.

Optional arguments:

* ``--schema SCHEMA`` the URL or path of the schema to validate against
* ``--check-urls`` check the HTTP status code if "format": "uri"
* ``--timeout TIMEOUT`` timeout (seconds) to GET a URL
* ``--verbose`` print items without validation errors

::

    cat tests/fixtures/* | ocdskit validate