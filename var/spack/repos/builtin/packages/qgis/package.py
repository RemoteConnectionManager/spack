from spack import *

class Qgis(Package):
    """qgis is an gis client program based on Qt and python.
    hints on install:
    https://htmlpreview.github.io/?https://raw.github.com/qgis/QGIS/master/doc/INSTALL.html#toc2
    """
    homepage = 'http://www.qgis.org/en/site/'
    url      = 'http://www.qgis.org/downloads/qgis-2.12.3.tar.bz2'

    version('2.13.3', 'f57ad5f04451d30032dbdd1836e0cb22', 
	     url='http://www.qgis.org/downloads/qgis-2.12.3.tar.bz2')
    
    depends_on('cmake')
    depends_on('qt@:4.8:')
    depends_on('geos')
    depends_on('python')
    depends_on('py-psycopg2')
    depends_on('sqlite')
    depends_on('expat')
    depends_on('py-sip')
    depends_on('py-qt')
    depends_on('qscintilla')
    depends_on('qwt')
    depends_on('gdal')
    depends_on('grass')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            def feature_to_bool(feature, on='ON', off='OFF'):
                if feature in spec:
                    return on
                return off

            def nfeature_to_bool(feature):
                return feature_to_bool(feature, on='OFF', off='ON')

            feature_args = std_cmake_args[:]
            feature_args.append('-DPARAVIEW_BUILD_QT_GUI:BOOL=%s' % feature_to_bool('+qt'))
            feature_args.append('-DPARAVIEW_ENABLE_PYTHON:BOOL=%s' % feature_to_bool('+python'))
            if '+python' in spec:
                feature_args.append('-DPYTHON_EXECUTABLE:FILEPATH=%s/bin/python' % spec['python'].prefix)
            feature_args.append('-DPARAVIEW_USE_MPI:BOOL=%s' % feature_to_bool('+mpi'))
            if '+mpi' in spec:
                feature_args.append('-DMPIEXEC:FILEPATH=%s/bin/mpiexec' % spec['mpi'].prefix)
            feature_args.append('-DVTK_ENABLE_TCL_WRAPPING:BOOL=%s' % feature_to_bool('+tcl'))
            feature_args.append('-DVTK_OPENGL_HAS_OSMESA:BOOL=%s' % feature_to_bool('+osmesa'))
            feature_args.append('-DVTK_USE_X:BOOL=%s' % nfeature_to_bool('+osmesa'))
            feature_args.append('-DVTK_RENDERING_BACKEND:STRING=%s' % feature_to_bool('+opengl2', 'OpenGL2', 'OpenGL'))

            feature_args.extend(std_cmake_args)

            if 'darwin' in self.spec.architecture:
                feature_args.append('-DVTK_USE_X:BOOL=OFF')
                feature_args.append('-DPARAVIEW_DO_UNIX_STYLE_INSTALLS:BOOL=ON')

            cmake('..',
                '-DCMAKE_INSTALL_PREFIX:PATH=%s' % prefix,
                '-DBUILD_TESTING:BOOL=OFF',
                '-DVTK_USER_SYSTEM_FREETYPE:BOOL=ON',
                '-DVTK_USER_SYSTEM_HDF5:BOOL=ON',
                '-DVTK_USER_SYSTEM_JPEG:BOOL=ON',
                '-DVTK_USER_SYSTEM_LIBXML2:BOOL=ON',
                '-DVTK_USER_SYSTEM_NETCDF:BOOL=ON',
                '-DVTK_USER_SYSTEM_TIFF:BOOL=ON',
                '-DVTK_USER_SYSTEM_ZLIB:BOOL=ON',
                *feature_args)
            make()
            make('install')
