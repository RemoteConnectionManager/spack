##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Bear(Package):
    """Bear is a tool that generates a compilation database for clang tooling
    from non-cmake build systems."""
    homepage = "https://github.com/rizsotto/Bear"
    url      = "https://github.com/rizsotto/Bear/archive/2.0.4.tar.gz"

    version('2.2.0', '87250cc3a9a697e7d1e8972253a35259')
    version('2.0.4', 'fd8afb5e8e18f8737ba06f90bd77d011')

    depends_on('cmake', type='build')
    depends_on("python")

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)

        make("all")
        make("install")
