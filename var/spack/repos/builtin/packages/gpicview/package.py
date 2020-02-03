# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gpicview(AutotoolsPackage):
    """GPicView - A Simple and Fast Image Viewer for X."""

    homepage = "http://lxde.sourceforge.net/gpicview/"
    url      = "https://sourceforge.net/projects/lxde/files/GPicView%20%28image%20Viewer%29/0.2.x/gpicview-0.2.5.tar.xz/download"

    version('0.2.5', sha256='38466058e53702450e5899193c4b264339959b563dd5cd81f6f690de32d82942')

    depends_on('perl-xml-parser', type='build')
    depends_on('gtkplus')
    depends_on('intltool')

    def install(self, spec, prefix):
        make()
        make('install')
