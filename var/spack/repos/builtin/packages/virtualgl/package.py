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
#
from spack import *


class Virtualgl(CMakePackage):
    """VirtualGL redirects 3D commands from a Unix/Linux OpenGL application
       onto a server-side GPU and converts the rendered 3D images into a video
       stream with which remote clients can interact to view and control the
       3D application in real time."""

    homepage = "http://www.virtualgl.org/Main/HomePage"
    url      = "http://downloads.sourceforge.net/project/virtualgl/2.5.2/VirtualGL-2.5.2.tar.gz"

    version('2.5.2', '1a9f404f4a35afa9f56381cb33ed210c')

    depends_on("libjpeg-turbo")
    depends_on("mesa-glu~mesa")

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
