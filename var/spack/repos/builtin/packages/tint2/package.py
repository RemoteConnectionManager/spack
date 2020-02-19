# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tint2(CMakePackage):
    """tint2 - lightweight panel/taskbar."""

    homepage = "https://www.mankier.com/1/tint2"
    git      = "https://gitlab.com/o9000/tint2.git"

    version('16.7', tag='v16.7')

    depends_on('cairo')
    depends_on('pango')
    depends_on('pkgconfig')
    depends_on('libx11')
    depends_on('libxdamage')
    depends_on('libxcomposite')
    depends_on('compositeproto')
    depends_on('fixesproto')
    depends_on('damageproto')
    depends_on('libxrandr')   
    depends_on('randrproto')
    depends_on('libxinerama')
    depends_on('xineramaproto')
    depends_on('startup-notification')
    depends_on('imlib2')
    depends_on('gtkplus')
    depends_on('glib')

    def cmake_args(self):
        """Populate cmake arguments for Tint2."""

        cmake_args = [
            '-DENABLE_BATTERY:BOOL=OFF',
            '-DENABLE_RSVG:BOOL=OFF',
            '-DENABLE_TINT2CONF=OFF'
        ]

        return cmake_args

