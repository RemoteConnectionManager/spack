# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRvcheck(RPackage):
    """Check latest release version of R and R package (both in 'CRAN',
    'Bioconductor' or 'Github')."""

    homepage = "https://cloud.r-project.org/package=rvcheck"
    url      = "https://cloud.r-project.org/src/contrib/rvcheck_0.0.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rvcheck"

    version('0.1.3', sha256='0b59986c1ccc5b89f8aca8fa7cf62d0b875719addb40e08dbda1791cfd334fc4')
    version('0.0.9', '7e9821de754577f94fdcbf7b02a20edc')

    depends_on('r@3.3.0:', when='@:0.1.1', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@0.1.3:', type=('build', 'run'))
    depends_on('r-rlang', when='@0.1.1:', type=('build', 'run'))
