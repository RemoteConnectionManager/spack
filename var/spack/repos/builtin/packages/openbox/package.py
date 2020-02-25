# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openbox(AutotoolsPackage):
    """Openbox is a highly configurable desktop window manager
       with extensive standards support. It allows you to control 
       almost every aspect of how you interact with your desktop."""

    homepage = "http://www.linuxfromscratch.org/blfs/view/svn/x/openbox.html"
    url      = "http://openbox.org/dist/openbox/openbox-3.6.1.tar.gz"

    version('3.6.1', sha256='8b4ac0760018c77c0044fab06a4f0c510ba87eae934d9983b10878483bde7ef7')

    depends_on('pango')
    depends_on('libx11')
    depends_on('libsm')
    depends_on('libice')

    def install(self, spec, prefix):
        make()
        make('install')

    def configure_args(self):
        spec = self.spec
        ldflags=[]
        cppflags=[]
        for dep in ['libsm', 'libice']:
            ldflags.append('-L'+spec[dep].prefix.lib)
            cppflags.append('-I'+spec[dep].prefix.include)
        config_args = [
            '--x-libraries={0}'.format(spec['libx11'].prefix.lib),
            '--x-includes={0}'.format(spec['libx11'].prefix.lib),
        ]
        config_args.append('LDFLAGS=' + ' '.join(ldflags))
        config_args.append('CPPFLAGS=' + ' '.join(cppflags))
        return config_args

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path("XDG_DATA_DIRS",
                               self.prefix.share)
        run_env.prepend_path("XDG_DATA_DIRS",
                             self.prefix.share)

