import numpy as np
from scipy.sparse import csr_matrix, _sparsetools
import scipy.sparse

try:
    # scipy >=1.8
    from scipy.sparse._sputils import upcast_char
except ImportError:
    # scipy <1.8
    from scipy.sparse.sputils import upcast_char

import pyamg.amg_core


class csr(csr_matrix):
    """
    New CSR class

    The purpose of this class is to redefine the matvec in scipy.sparse
    """
    def _mul_vector(self, other):
        """
        Identical to scipy.sparse with an in internal call to
        pyamg.amg_core.sparse.csr_matvec
        """
        M, N = self.shape

        # output array
        result = np.zeros(M, dtype=upcast_char(self.dtype.char,
                                               other.dtype.char))

        #scipy.sparse._sparsetools.csr_matvec(M, N, self.indptr, self.indices, self.data, other, result)
        pyamg.amg_core.sparse.csr_matvec(M, N, self.indptr, self.indices, self.data, other, result)

        return result


csr.__doc__ += csr_matrix.__doc__
