# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import datetime

from .. import utils


__all__ = ('cli_loader',)


@utils.with_cursor
def cli_command(cursor, migrations_directory='', version=None, **kwargs):
    cursor.execute("""\
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT NOT NULL,
            applied TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )""")
    cursor.execute("""\
        DELETE FROM schema_migrations""")
    versions = []
    if version is None:
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    else:
        timestamp = str(version)
    for version, name in utils.get_migrations(migrations_directory):
        if version <= timestamp:
            versions.append((version,))
    cursor.executemany("""\
        INSERT INTO schema_migrations VALUES (%s)
        """, versions)
    print('Schema migrations initialized.')


def cli_loader(parser):
    parser.add_argument('--version', type=int,
                        help='Set the schema version to VERSION, '
                             'default current timestamp')
    return cli_command
