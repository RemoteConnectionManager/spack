from spack import *

class PyPsycopg2(Package):
    """PostgreSQL adapter for Python ."""
    homepage = "http://initd.org/psycopg/"
    url      = "http://initd.org/psycopg/tarballs/PSYCOPG-2-6/psycopg2-2.6.1.tar.gz"

    version('2.6.1', '842b44f8c95517ed5b792081a2370da1')

    extends('python')
    depends_on('postgresql')
    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
