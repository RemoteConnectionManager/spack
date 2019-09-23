# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Imlib2(AutotoolsPackage):
    """imlib2 is a graphics library for fast file loading, 
       saving, rendering and manipulation."""

    homepage = "http://www.linuxfromscratch.org/blfs/view/svn/x/imlib2.html"
    url      = "https://downloads.sourceforge.net/enlightenment/imlib2-1.5.1.tar.bz2"

    version('1.5.1', sha256='fa4e57452b8843f4a70f70fd435c746ae2ace813250f8c65f977db5d7914baae')

    depends_on('libx11')

    def install(self, spec, prefix):
        make()
        make('install')
