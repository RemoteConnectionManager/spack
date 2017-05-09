##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os


class LibjpegTurbo(AutotoolsPackage):
    """libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to
       accelerate baseline JPEG compression and decompression. libjpeg is a
       library that implements JPEG image encoding, decoding and
       transcoding."""

    homepage = "http://libjpeg-turbo.virtualgl.org"
    url      = "http://downloads.sourceforge.net/libjpeg-turbo/libjpeg-turbo-1.3.1.tar.gz"

    version('1.5.1', '55deb139b0cac3c8200b75d485fc13f3')
    version('1.5.0', '3fc5d9b6a8bce96161659ae7a9939257')
    version('1.4.2', '86b0d5f7507c2e6c21c00219162c3c44')
    version('1.3.1', '2c3a68129dac443a72815ff5bb374b05')

    provides('jpeg')
    variant('java', default=False, description='Enable Java build')

    # Can use either of these. But in the current version of the package
    # only nasm is used. In order to use yasm an environmental variable
    # NASM must be set.
    # TODO: Implement the selection between two supported assemblers.
    # depends_on("yasm", type='build')
    depends_on("nasm", type='build')
    depends_on('jdk', when='+java', type='build')

    def configure_args(self):
        args = []
        if '+java' in self.spec:
            args.append('--with-java')
            # args.append('--with-java=' + self.spec['jdk'].prefix)
        return args

    def setup_environment(self, spack_env, run_env):
        if '+java' in self.spec:
            spack_env.set(
                'JNI_CFLAGS',
                '-I' + os.path.join(self.spec['jdk'].prefix, 'include') +
                ' ' + '-I' +
                os.path.join(self.spec['jdk'].prefix, 'include', 'linux'),
                separator=' ')
