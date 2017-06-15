##############################################################################
# Copyright (c) 2017 Mark Olesen, OpenCFD Ltd.
#
# This file was authored by Mark Olesen <mark.olesen@esi-group.com>
# and is released as part of spack under the LGPL license.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for the LLNL notice and the LGPL.
#
# License
# -------
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
#
# Legal Notice
# ------------
# OPENFOAM is a trademark owned by OpenCFD Ltd
# (producer and distributor of the OpenFOAM software via www.openfoam.com).
# The trademark information must remain visible and unadulterated in this
# file and via the "spack info" and comply with the term set by
# http://openfoam.com/legal/trademark-policy.php
#
# This file is not part of OpenFOAM, nor does it constitute a component of an
# OpenFOAM distribution.
#
##############################################################################
#
# Notes
# - The openfoam-org package is a modified version of the openfoam-com package.
#   If changes are needed here, consider if they should also be applied there.
#
# - Building with boost/cgal is not included, since some of the logic is not
#   entirely clear and thus untested.
# - Resolution of flex, zlib needs more attention (within OpenFOAM)
#
# - mpi handling: WM_MPLIB=SYSTEMMPI and use spack to populate the prefs.sh
#   for it.
#   Also provide wmake rules for special purpose 'USER' and 'USERMPI'
#   mpi implementations, in case these are required.
#
##############################################################################
from spack import *
from spack.environment import *
import llnl.util.tty as tty

import multiprocessing
import glob
import re
import shutil
import os
from os.path import isdir, isfile
from spack.pkg.builtin.openfoam_com import *


class OpenfoamOrg(Package):
    """OpenFOAM is a GPL-opensource C++ CFD-toolbox.
    The openfoam.org release is managed by the OpenFOAM Foundation Ltd as
    a licensee of the OPENFOAM trademark.
    This offering is not approved or endorsed by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    """

    homepage = "http://www.openfoam.org/"
    baseurl  = "https://github.com/OpenFOAM"
    url      = "https://github.com/OpenFOAM/OpenFOAM-4.x/archive/version-4.1.tar.gz"

    version('4.1', '318a446c4ae6366c7296b61184acd37c',
            url=baseurl + '/OpenFOAM-4.x/archive/version-4.1.tar.gz')

    variant('int64', default=False,
            description='Compile with 64-bit labels')
    variant('float32', default=False,
            description='Compile with 32-bit scalar (single-precision)')

    variant('source', default=True,
            description='Install library/application sources and tutorials')

    #: Map spack compiler names to OpenFOAM compiler names
    #  By default, simply capitalize the first letter
    compiler_mapping = {'intel': 'icc'}

    provides('openfoam')
    depends_on('mpi')
    depends_on('zlib')
    depends_on('flex@:2.6.1')  # <- restriction due to scotch
    depends_on('cmake', type='build')

    # Require scotch with ptscotch - corresponds to standard OpenFOAM setup
    depends_on('scotch~int64+mpi', when='~int64')
    depends_on('scotch+int64+mpi', when='+int64')

    # General patches
    patch('openfoam-site.patch')

    # Version-specific patches
    patch('openfoam-etc-41.patch')

    # Some user settings, to be adjusted manually or via variants
    foam_cfg = {
        'WM_COMPILER':        'Gcc',  # <- %compiler
        'WM_ARCH_OPTION':     '64',   # (32/64-bit on x86_64)
        'WM_LABEL_SIZE':      '32',   # <- +int64
        'WM_PRECISION_OPTION': 'DP',  # <- +float32
        'WM_COMPILE_OPTION':  'SPACKOpt',   # Do not change
        'WM_MPLIB':           'SYSTEMMPI',  # Use system mpi for spack
    }

    # The system description is frequently needed
    foam_sys = {
        'WM_ARCH':      None,
        'WM_COMPILER':  None,
        'WM_OPTIONS':   None,
    }

    # Content for etc/prefs.{csh,sh}
    etc_prefs = {}

    # Content for etc/config.{csh,sh}/ files
    etc_config = {}

    build_script = './spack-Allwmake'  # <- Generated by patch() method.
    # phases = ['configure', 'build', 'install']
    # build_system_class = 'OpenfoamCom'

    # Add symlinks into bin/, lib/ (eg, for other applications)
    extra_symlinks = False

    def setup_environment(self, spack_env, run_env):
        run_env.set('WM_PROJECT_DIR', self.projectdir)

    @property
    def _canonical(self):
        """Canonical name for this package and version"""
        return 'OpenFOAM-{0}'.format(self.version)

    @property
    def projectdir(self):
        """Absolute location of project directory: WM_PROJECT_DIR/"""
        return join_path(self.prefix, self._canonical)  # <- prefix/canonical

    @property
    def etc(self):
        """Absolute location of the OpenFOAM etc/ directory"""
        return join_path(self.projectdir, 'etc')

    @property
    def archbin(self):
        """Relative location of architecture-specific executables"""
        return join_path('platforms', self.wm_options, 'bin')

    @property
    def archlib(self):
        """Relative location of architecture-specific libraries"""
        return join_path('platforms', self.wm_options, 'lib')

    @property
    def wm_options(self):
        """The architecture+compiler+options for OpenFOAM"""
        opts = self.set_openfoam()
        return opts

    @property
    def rpath_info(self):
        """Define 'SPACKOpt' compiler optimization file to have wmake
        use spack information with minimum modifications to OpenFOAM
        """
        build_libpath   = join_path(self.stage.source_path, self.archlib)
        install_libpath = join_path(self.projectdir, self.archlib)

        # 'DBUG': rpaths
        return '{0}{1} {2}{3}'.format(
            self.compiler.cxx_rpath_arg, install_libpath,
            self.compiler.cxx_rpath_arg, build_libpath)

    def openfoam_arch(self):
        """Return an architecture value similar to what OpenFOAM does in
        etc/config.sh/settings, but slightly more generous.
        Uses and may adjust foam_cfg[WM_ARCH_OPTION] as a side-effect
        """
        # spec.architecture.platform is like `uname -s`, but lower-case
        platform = self.spec.architecture.platform

        # spec.architecture.target is like `uname -m`
        target   = self.spec.architecture.target

        if platform == 'linux':
            if target == 'i686':
                self.foam_cfg['WM_ARCH_OPTION'] = '32'  # Force consistency
            elif target == 'x86_64':
                if self.foam_cfg['WM_ARCH_OPTION'] == '64':
                    platform += '64'
            elif target == 'ia64':
                platform += 'ia64'
            elif target == 'armv7l':
                platform += 'ARM7'
            elif target == ppc64:
                platform += 'PPC64'
            elif target == ppc64le:
                platform += 'PPC64le'
        elif platform == 'darwin':
            if target == 'x86_64':
                platform += 'Intel'
                if self.foam_cfg['WM_ARCH_OPTION'] == '64':
                    platform += '64'
        # ... and others?
        return platform

    def openfoam_compiler(self):
        """Capitalized version of the compiler name, which usually corresponds
        to how OpenFOAM will camel-case things.
        Use compiler_mapping to handing special cases.
        Also handle special compiler options (eg, KNL)
        """
        comp = self.compiler.name
        if comp in self.compiler_mapping:
            comp = self.compiler_mapping[comp]
        comp = comp.capitalize()

        if '+knl' in self.spec:
            comp += 'KNL'
        return comp

    def set_openfoam(self):
        """Populate foam_cfg, foam_sys according to
        variants, architecture, compiler.
        Returns WM_OPTIONS.
        """
        # Run once
        opts = self.foam_sys['WM_OPTIONS']
        if opts:
            return opts

        wm_arch     = self.openfoam_arch()
        wm_compiler = self.openfoam_compiler()
        compileOpt  = self.foam_cfg['WM_COMPILE_OPTION']

        # Insist on a wmake rule for this architecture/compiler combination
        archCompiler  = wm_arch + wm_compiler
        compiler_rule = join_path(
            self.stage.source_path, 'wmake', 'rules', archCompiler)

        if not isdir(compiler_rule):
            raise RuntimeError(
                'No wmake rule for {0}'.format(archCompiler))
        if not re.match(r'.+Opt$', compileOpt):
            raise RuntimeError(
                "WM_COMPILE_OPTION={0} is not type '*Opt'".format(compileOpt))

        # Adjust for variants
        self.foam_cfg['WM_LABEL_SIZE'] = (
            '64' if '+int64'   in self.spec else '32'
        )
        self.foam_cfg['WM_PRECISION_OPTION'] = (
            'SP' if '+float32' in self.spec else 'DP'
        )

        # ----
        # WM_LABEL_OPTION=Int$WM_LABEL_SIZE
        # WM_OPTIONS=$WM_ARCH$WM_COMPILER$WM_PRECISION_OPTION$WM_LABEL_OPTION$WM_COMPILE_OPTION
        # ----
        self.foam_sys['WM_ARCH']     = wm_arch
        self.foam_sys['WM_COMPILER'] = wm_compiler
        self.foam_cfg['WM_COMPILER'] = wm_compiler  # For bashrc,cshrc too
        self.foam_sys['WM_OPTIONS']  = ''.join([
            wm_arch,
            wm_compiler,
            self.foam_cfg['WM_PRECISION_OPTION'],
            'Int', self.foam_cfg['WM_LABEL_SIZE'],  # Int32/Int64
            compileOpt
        ])
        return self.foam_sys['WM_OPTIONS']

    def patch(self):
        """Adjust OpenFOAM build for spack. Where needed, apply filter as an
        alternative to normal patching.
        """
        self.set_openfoam()  # May need foam_cfg/foam_sys information

        # This is fairly horrible.
        # The github tarfiles have weird names that do not correspond to the
        # canonical name. We need to rename these, but leave a symlink for
        # spack to work with.
        #
        # Note that this particular OpenFOAM release requires absolute
        # directories to build correctly!
        parent   = os.path.dirname(self.stage.source_path)
        original = os.path.basename(self.stage.source_path)
        target   = self._canonical
        with working_dir(parent):
            if original != target and not os.path.lexists(target):
                os.rename(original, target)
                os.symlink(target, original)
                tty.info('renamed {0} -> {1}'.format(original, target))

        # Avoid WM_PROJECT_INST_DIR for ThirdParty, site or jobControl.
        # Use openfoam-site.patch to handle jobControl, site.
        #
        # Filter (not patch) bashrc,cshrc for additional flexibility
        wm_setting = {
            'WM_THIRD_PARTY_DIR':
            r'$WM_PROJECT_DIR/ThirdParty #SPACK: No separate third-party',
            'WM_VERSION': self.version,    # consistency
            'FOAMY_HEX_MESH': '',          # This is horrible (unset variable?)
        }

        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            wm_setting,
            posix=join_path('etc', 'bashrc'),
            cshell=join_path('etc', 'cshrc'))

        # Build wrapper script
        with open(self.build_script, 'w') as out:
            out.write(
                """#!/bin/bash
. $PWD/etc/bashrc ''  # No arguments
mkdir -p $FOAM_APPBIN $FOAM_LIBBIN 2>/dev/null  # Allow interrupt
echo Build openfoam with SPACK
echo WM_PROJECT_DIR = $WM_PROJECT_DIR
./Allwmake $@
#
""")
        set_executable(self.build_script)
        self.configure(self.spec, self.prefix)  # Should be a separate phase

    def configure(self, spec, prefix):
        """Make adjustments to the OpenFOAM configuration files in their various
        locations: etc/bashrc, etc/config.sh/FEATURE and customizations that
        don't properly fit get placed in the etc/prefs.sh file (similiarly for
        csh).
        """
        self.set_openfoam()  # Need foam_cfg/foam_sys information

        # Some settings for filtering bashrc, cshrc
        wm_setting = {}
        wm_setting.update(self.foam_cfg)

        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            wm_setting,
            posix=join_path('etc', 'bashrc'),
            cshell=join_path('etc', 'cshrc'))

        # MPI content, with absolute paths
        content = mplib_content(spec)

        # Content for etc/prefs.{csh,sh}
        self.etc_prefs = {
            r'MPI_ROOT': spec['mpi'].prefix,  # Absolute
            r'MPI_ARCH_FLAGS': '"%s"' % content['FLAGS'],
            r'MPI_ARCH_INC':   '"%s"' % content['PINC'],
            r'MPI_ARCH_LIBS':  '"%s"' % content['PLIBS'],
        }

        # Content for etc/config.{csh,sh}/ files
        self.etc_config = {
            'CGAL': {},
            'scotch': {},
            'metis': {},
            'paraview': [],
        }

        if True:
            self.etc_config['scotch'] = {
                'SCOTCH_ARCH_PATH': spec['scotch'].prefix,
                # For src/parallel/decompose/Allwmake
                'SCOTCH_VERSION': 'scotch-{0}'.format(spec['scotch'].version),
            }

        # Write prefs files according to the configuration.
        # Only need prefs.sh for building, but install both for end-users
        if self.etc_prefs:
            write_environ(
                self.etc_prefs,
                posix=join_path('etc', 'prefs.sh'),
                cshell=join_path('etc', 'prefs.csh'))

        # Adjust components to use SPACK variants
        for component, subdict in self.etc_config.items():
            write_environ(
                subdict,
                posix=join_path('etc', 'config.sh',  component),
                cshell=join_path('etc', 'config.csh', component))

        archCompiler  = self.foam_sys['WM_ARCH'] + self.foam_sys['WM_COMPILER']
        compileOpt    = self.foam_cfg['WM_COMPILE_OPTION']
        general_rule  = join_path('wmake', 'rules', 'General')
        compiler_rule = join_path('wmake', 'rules', archCompiler)
        generate_mplib_rules(general_rule, self.spec)
        generate_compiler_rules(compiler_rule, compileOpt, self.rpath_info)
        # Record the spack spec information
        with open("log.spack-spec", 'w') as outfile:
            outfile.write(spec.tree())

    def build(self, spec, prefix):
        """Build using the OpenFOAM Allwmake script, with a wrapper to source
        its environment first.
        """
        self.set_openfoam()  # Force proper population of foam_cfg/foam_sys
        args = []
        if self.parallel:  # Build in parallel? - pass via the environment
            os.environ['WM_NCOMPPROCS'] = str(self.make_jobs) \
                if self.make_jobs else str(multiprocessing.cpu_count())
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the projectdir (== prefix/name-version)"""
        self.build(spec, prefix)  # Should be a separate phase
        opts = self.wm_options

        mkdirp(self.projectdir)
        projdir = os.path.basename(self.projectdir)
        wm_setting = {
            'WM_PROJECT_INST_DIR': os.path.dirname(self.projectdir),
            'WM_PROJECT_DIR': join_path('$WM_PROJECT_INST_DIR', projdir),
        }

        # Retain build log file
        out = "spack-build.out"
        if isfile(out):
            install(out, join_path(self.projectdir, "log." + opts))

        # All top-level files, except spack build info and possibly Allwmake
        if '+source' in spec:
            ignored = re.compile(r'^spack-.*')
        else:
            ignored = re.compile(r'^(Allwmake|spack-).*')

        files = [
            f for f in glob.glob("*") if isfile(f) and not ignored.search(f)
        ]
        for f in files:
            install(f, self.projectdir)

        # Having wmake without sources is actually somewhat pointless...
        dirs = ['bin', 'etc', 'wmake']
        if '+source' in spec:
            dirs.extend(['applications', 'src', 'tutorials'])

        for d in dirs:
            install_tree(
                d,
                join_path(self.projectdir, d))

        dirs = ['platforms']
        if '+source' in spec:
            dirs.extend(['doc'])

        # Install platforms (and doc) skipping intermediate targets
        ignored = ['src', 'applications', 'html', 'Guides']
        for d in dirs:
            install_tree(
                d,
                join_path(self.projectdir, d),
                ignore=shutil.ignore_patterns(*ignored))

        rewrite_environ_files(  # Adjust etc/bashrc and etc/cshrc
            wm_setting,
            posix=join_path(self.etc, 'bashrc'),
            cshell=join_path(self.etc, 'cshrc'))
        self.install_links()

    def install_links(self):
        """Add symlinks into bin/, lib/ (eg, for other applications)"""
        if not self.extra_symlinks:
            return

        # ln -s platforms/linux64GccXXX/lib lib
        with working_dir(self.projectdir):
            if isdir(self.archlib):
                os.symlink(self.archlib, 'lib')

        # (cd bin && ln -s ../platforms/linux64GccXXX/bin/* .)
        with working_dir(join_path(self.projectdir, 'bin')):
            for f in [
                f for f in glob.glob(join_path('..', self.archbin, "*"))
                if isfile(f)
            ]:
                os.symlink(f, os.path.basename(f))

# -----------------------------------------------------------------------------
