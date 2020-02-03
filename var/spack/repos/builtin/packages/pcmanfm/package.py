# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Pcmanfm(AutotoolsPackage):
    """Man File Manager (PCManFM) is a file manager application 
       developed by Hong Jen Yee from Taiwan which is meant to be 
       a replacement for GNOME Files, Dolphin and Thunar.
       PCManFM is the standard file manager in LXDE, also developed 
       by the same author in conjunction with other developers."""

    homepage = "https://wiki.lxde.org/it/PCManFM"
    url      = "https://downloads.sourceforge.net/pcmanfm/pcmanfm-1.3.1.tar.xz"

    version('1.3.1', 'd32ad2c9c7c52bff2004bbc120b53420')

    depends_on('pkgconfig', type='build')
    depends_on('perl-xml-parser', type='build')
    depends_on('libx11')
    depends_on('libxinerama')
    depends_on('lxde-libfm')
    depends_on('intltool')

    def install(self, spec, prefix):
        make()
        make('install')
