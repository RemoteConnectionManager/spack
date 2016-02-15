# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install qwt
#
# You can always get back here to change things with:
#
#     spack edit qwt
#
# See the spack documentation for more information on building
# packages.
#
from spack import *
import shutil

class Qwt(Package):
    """Qt Widgets for Technical Applications """
    homepage = "http://qwt.sourceforge.net/"
    url      = "http://heanet.dl.sourceforge.net/project/qwt/qwt/6.1.2/qwt-6.1.2.tar.bz2"

    version('6.1.2', '9c88db1774fa7e3045af063bbde44d7d')

    depends_on("qt")

    def patch(self):
        shutil.copy('qwtconfig.pri', 'qwtconfig.pri.orig')
        mf = FileFilter('qwtconfig.pri')
        mf.filter('\$\$\[QT_INSTALL_PREFIX\]', self.prefix)
        mf.filter('/usr/local/qwt-\$\$QWT_VERSION', self.prefix)
        

    def install(self, spec, prefix):
        qmake = Executable(join_path(spec['qt'].prefix.bin, 'qmake'))
        qmake('qwt.pro')
        make()
        make("install")
