from numpy import diag_indices_from, empty_like, finfo, sqrt
from numpy.linalg import LinAlgError, cholesky


def check_definite_positiveness(A):
    """Check if ``A`` is a definite positive matrix.

    Args:
        A (array_like): Matrix.

    Returns:
        bool: ``True`` if ``A`` is definite positive; ``False`` otherwise.
    """
    B = empty_like(A)
    B[:] = A
    B[diag_indices_from(B)] += sqrt(finfo(float).eps)
    try:
        cholesky(B)
    except LinAlgError:
        return False
    return True


def check_symmetry(A):
    """Check if ``A`` is a symmetric matrix.

    Args:
        A (array_like): Matrix.

    Returns:
        bool: ``True`` if ``A`` is symmetric; ``False`` otherwise.
    """
    return abs(A - A.T).max() < sqrt(finfo(float).eps)
