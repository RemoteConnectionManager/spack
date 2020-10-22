# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Virtualgl(CMakePackage):
    """VirtualGL redirects 3D commands from a Unix/Linux OpenGL application
       onto a server-side GPU and converts the rendered 3D images into a video
       stream with which remote clients can interact to view and control the
       3D application in real time."""

    homepage = "http://www.virtualgl.org/Main/HomePage"
    url      = "http://downloads.sourceforge.net/project/virtualgl/2.5.2/VirtualGL-2.5.2.tar.gz"

    version('2.6.4', sha256='39978f737ffe73e426e9a921486b9f6cee9c9b9ab9e82d2ae4e2ffe3b27398e5')
    version('2.5.2', sha256='4f43387678b289a24139c5b7c3699740ca555a9f10011c979e51aa4df2b93238')

    depends_on("jpeg")
    depends_on("glu")
    depends_on("libxcb")
    depends_on("xcb-util-keysyms")
    depends_on("libx11")
    depends_on("libxau")
    depends_on("libxrender")
    depends_on("libxrandr")
    depends_on("libxinerama")
    depends_on("libxft")
    depends_on("libxmu")
    depends_on("libxpm")
    depends_on("libxscrnsaver")
    depends_on("libxv")
    depends_on("libxt")
    depends_on("libxres")
    depends_on("libxcomposite")
    depends_on("libxcursor")
    depends_on("libxdamage")
    depends_on("libxtst")
    depends_on("libxkbfile")
    depends_on("libxxf86vm")
    depends_on("libxxf86misc")

    def cmake_args(self):
        spec = self.spec

        cmake_args = [
            '-DVGL_FAKEOPENCL=OFF'
        ]
        return cmake_args

