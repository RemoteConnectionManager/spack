from spack import *

class Petsc(Package):
    """PETSc is a suite of data structures and routines for the
       scalable (parallel) solution of scientific applications modeled by
       partial differential equations."""

    homepage = "http://www.mcs.anl.gov/petsc/index.html"
    url      = "http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.5.3.tar.gz"
 
    version('3.6.3', '91dd3522de5a5ef039ff8f50800db606')
    version('3.5.3', 'd4fd2734661e89f18ac6014b5dd1ef2f')
    version('3.5.2', 'ad170802b3b058b5deb9cd1f968e7e13')
    version('3.5.1', 'a557e029711ebf425544e117ffa44d8f')

    variant('boost', default=True, description='Build with boost')
    variant('shared', default=False, description='Build shared')
    variant('fortran', default=False, description='Build with fortran')
    variant('debug', default=True, description='Build with debugging')


    depends_on("python @2.6:2.9")   # requires Python for building

    depends_on("boost", when='+boost')
    depends_on("blas")
    depends_on("lapack")
    depends_on("hypre")
    depends_on("parmetis")
    depends_on("metis")
    depends_on("hdf5+mpi")
    depends_on("mpi")

    def install(self, spec, prefix):
        def feature_to_bool(feature, on=1, off=0):
            if feature in spec:
                return on
            return off

        options = ['-prefix=%s' % prefix]
        if '+boost' in spec:
            options.append("--with-boost-dir=%s"              % spec['boost'].prefix)
        if '+fortran' in spec:
            options.append("--with-fortran=%s" % feature_to_bool('+fortran'))
            options.append("--with-fortran-interfaces=%s" % feature_to_bool('+fortran'))
        options.append("--with-shared-libraries=%s" % feature_to_bool('+shared'))
        options.append("--with-debugging=%s" % feature_to_bool('+debug'))

        configure("--prefix=%s" % prefix,
                  "--with-blas-lib=%s/libblas.a"     % spec['blas'].prefix.lib,
                  "--with-lapack-lib=%s/liblapack.a" % spec['lapack'].prefix.lib,
                  "--with-boost-dir=%s"              % spec['boost'].prefix,
                  "--with-hypre-dir=%s"              % spec['hypre'].prefix,
                  "--with-parmetis-dir=%s"           % spec['parmetis'].prefix,
                  "--with-metis-dir=%s"              % spec['metis'].prefix,
                  "--with-hdf5-dir=%s"               % spec['hdf5'].prefix,
                  "--with-mpi-dir=%s"                % spec['mpi'].prefix,
                  "--with-shared-libraries=%s" % feature_to_bool('+shared'),
                  "--with-debugging=%s" % feature_to_bool('+debug'))

        # PETSc has its own way of doing parallel make.
        make('MAKE_NP=%s' % make_jobs, parallel=False)
        make("install")
