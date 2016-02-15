# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install qscintilla
#
# You can always get back here to change things with:
#
#     spack edit qscintilla
#
# See the spack documentation for more information on building
# packages.
#
from spack import *
import shutil

class Qscintilla(Package):
    """QScintilla is a port to Qt of Neil Hodgson's Scintilla C++ editor control."""
    homepage = "https://riverbankcomputing.com/software/qscintilla/intro"
    url      = "http://sourceforge.net/projects/pyqt/files/QScintilla2/QScintilla-2.9/QScintilla-gpl-2.9.tar.gz"

    version('2.9', '24659879edf9786f41a9b9268ce3c817')

    variant('exampleapp', default=True)

    depends_on("qt")

    def patch(self):
        with working_dir('Qt4Qt5'):
            shutil.copy('qscintilla.pro', 'qscintilla_patch.pro')
            mf = FileFilter('qscintilla_patch.pro')

            mf.filter('\$\$\[QT_INSTALL_HEADERS\]', join_path(self.prefix,'include'))
            mf.filter('\$\$\[QT_INSTALL_LIBS\]', join_path(self.prefix,'lib'))
            mf.filter('\$\$\[QT_INSTALL_TRANSLATIONS\]', join_path(self.prefix,'translations'))
            mf.filter('\$\$\[QT_INSTALL_DATA\]', self.prefix)

    def install(self, spec, prefix):
        qmake = Executable(join_path(spec['qt'].prefix.bin, 'qmake'))
        with working_dir('Qt4Qt5'):
            qmake('qscintilla_patch.pro')
            make()
            make("install")
        if '+exampleapp' in spec:
            with working_dir('example-Qt4Qt5'):
                qmake('application.pro')
                make()
                mkdirp(prefix.bin)
                install('application', prefix.bin)
    