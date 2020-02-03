# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Leafpad(AutotoolsPackage):
    """leafpad - GTK+ based simple text editor."""

    homepage = "http://tarot.freeshell.org/leafpad/"
    url      = "http://savannah.nongnu.org/download/leafpad/leafpad-0.8.17.tar.gz"

    version('0.8.18.1', sha256='959d22ae07f22803bc66ff40d373a854532a6e4732680bf8a96a3fbcb9f80a2c')

    depends_on('gtkplus')
    depends_on('intltool')

    def install(self, spec, prefix):
        make()
        make('install')
