"""
The squareExtensions module provides
two special classes to give exact representations of the values
involved when computing a cusp cross section.

The method find_shapes_as_complex_sqrt_lin_combinations returns a list of
shapes as ComplexSqrtLinCombination's. This can be used as input to
CuspCrossSection. The outputs of CuspCrossSection, including the tilts, will
then be of type SqrtLinCombination.

Consider the real number field N generated by the real and imaginary part of
the shapes. The edge lengths and the factors used to normalize the cusp areas
will be square roots in N and thus the tilts will be N-linear combinations of
square roots in N. To avoid computing in a massive tower of square extensions
of N, we implement SqrtLinCombination here that provides a special
implementation of the == operator.
"""

from ..sage_helper import _within_sage, sage_method, SageNotAvailable

__all__ = ['find_shapes_as_complex_sqrt_lin_combinations',
           'SqrtLinCombination',
           'ComplexSqrtLinCombination']

if _within_sage:
    from sage.rings.complex_interval_field import ComplexIntervalField
    from sage.rings.real_mpfi import RealIntervalField
    from sage.rings.integer import Integer
    from sage.rings.rational import Rational
    from sage.rings.number_field.number_field_element import NumberFieldElement
    from sage.rings.complex_number import create_ComplexNumber
    from sage.functions.other import sqrt

    _Zero = Integer(0)
    _One = Integer(1)

    from ..snap import find_field

from .realAlgebra import field_containing_real_and_imaginary_part_of_number_field

def eval_number_field_elt(elt, root):
    # SageMath 7.6 can no longer evaluate a rational polynomial on an
    # arbitrary type that supports the basic arithmetic
    # operations. Rather, one can only evaluate on inputs that have
    # been registered into its coercion model.  Thus we have to
    # evaluate things manually.
    if elt.is_zero():
        return _Zero
    poly = elt.lift()
    R = poly.base_ring()
    coeffs = poly.coefficients()
    exps = poly.exponents()
    powers = [R(1)]
    for i in range(max(exps)):
        powers.append(powers[-1]*root)
    return sum(c*powers[e] for (c, e) in zip(coeffs, exps))

import operator

# One problem in verifying canonical cell decomposition is that we need to do
# computations in the real field which contains the real and imaginary part
# of the shape field.
#
# Our first try was using Sage's QQbar which was suggested here:
# http://ask.sagemath.org/question/25822/number-field-containing-realimaginary-part-of-algebraic-number/
# But turns out way too slow.
#
# Next, we tried to use the LLL-algorithm applied to the real and imaginary part
# of the generator of the shape field (effectively applying LLL twice, once to
# find the shape field and then the field containing the real and imaginary part
# of the shape field).
# This is implemented in
#    _field_containing_real_and_imaginary_part_of_algebraic_number_LLL.
# This was still very slow and failed on t11669 and 9 manifolds with 9 tetrahedra.
# 
# The fastest implementation so far is in realAlgebra. The implementation there
# turns the one complex equation p(z) = 0 definining the number field into two
# real equations for the real and imaginary part of the complex equation and
# then uses the resultant to find exact solutions.

@sage_method
def find_shapes_as_complex_sqrt_lin_combinations(M, prec, degree):
    """
    Given a manifold M, use snap (which uses LLL-algorithm) with the given
    decimal precision and maximal degree to find exact values for the shapes'
    real and imaginary part. Return the shapes as list of
    ComplexSqrtLinCombination's. Return None on failure.

    Example::

       sage: from snappy import Manifold
       sage: M=Manifold("m412")
       sage: find_shapes_as_complex_sqrt_lin_combinations(M, 200, 10)
       [ComplexSqrtLinCombination((1/2) * sqrt(1), (x - 1/2) * sqrt(1)), ComplexSqrtLinCombination((1/2) * sqrt(1), (x - 1/2) * sqrt(1)), ComplexSqrtLinCombination((1/2) * sqrt(1), (x - 1/2) * sqrt(1)), ComplexSqrtLinCombination((1/2) * sqrt(1), (x - 1/2) * sqrt(1)), ComplexSqrtLinCombination((1/2) * sqrt(1), (x - 1/2) * sqrt(1))]
    """

    # We need to find the NumberField that contains the real and imaginary
    # parts of all shapes.

    # First we try to find the field containing the complex shapes:
    complex_data = M.tetrahedra_field_gens().find_field(prec, degree)
    if not complex_data:
        return None

    # Split Snap's result
    # complex_root is an ApproximateAlgebraicNumber, the root of the
    #      NumberField's defining polynomial
    # exact_complex_shapes are elements in a Sage NumberField
    complex_number_field, complex_root, exact_complex_shapes = complex_data

    # We now have a generator (complex_root) for the NumberField 
    # containing the shapes.
    # Next, we need to find the NumberField containing the real and imaginary
    # part of this generator.

    real_result = field_containing_real_and_imaginary_part_of_number_field(
        complex_number_field)

    if not real_result:
        return None

    real_number_field, real_part, imag_part = real_result

    # Caches the values of 
    #      nf.gen_embedding()
    # and  RealIntervalField(prec)(nf.gen_embedding())
    # for different precision prec where nf is the NumberField real_number_field
    # in which real_part and imag_part live.
    #
    # This is for speed only. See _get_interval_embedding_from_cache for
    # details.
    embed_cache = {}
    
    # The generator of the shape field as the desired return type
    exact_complex_root = ComplexSqrtLinCombination(real_part, imag_part,
                                                   embed_cache = embed_cache)

    # All shapes are given as polynomials in the generator,
    # so translate them to be of the desired return type
    return [ eval_number_field_elt(exact_complex_shape, exact_complex_root)
             for exact_complex_shape in exact_complex_shapes ]

class SqrtLinCombination(object):
    """
    A class representing a linear combination

        c_1 * sqrt(r_1) + c_2 * sqrt(r_2) + ... + c_n * sqrt(r_n)

    where c_i and r_i have to be of type Integer, Rational or elements
    of the same Sage NumberField with a real embedding (Caution: this is
    assumed but not checked!) such that all r_i are positive (Caution: this is
    not checked during construction!).

    It implements +, -, * where one of the operators is allowed to be an
    integer or rational.

    / is only implemented when the denominator has only one term c_1 * sqrt(1).
    sqrt is only implemented for c_1 * sqrt(1) and it is not checked that
    c_1 is positive.

    == is implemented, but the other comparison operators are not: casting to
    a RealIntervalField is implemented instead and the user can compare the
    intervals.

    The == operator is implemented by first reducing A == B to D == 0 and then
    converting to a different data type (_FactorizedSqrtLinCombination) that can
    represent linear combinations::

      D =     c_1 * sqrt(r_{1,1}) * sqrt(r_{1,2}) * ... * sqrt(r_{1,k_1})
            + c_2 * sqrt(r_{2,1}) * sqrt(r_{2,2}) * ... * sqrt(r_{2,k_2})
            + ...
            + c_n * sqrt(r_{n,1}) * sqrt(r_{n,2}) * ... * sqrt(r_{n,k_n})

    by just trivially setting
       k_i = 0                       when r_i = 1 and
       r_{i,1} = r_i and k_1 = 1     otherwise.

    For this data type, multiplying two sqrt(r_{i,j}) with equal r_{i,j} will
    cancel the two sqrt's and apply the common r_{i,j} to the c_i of the result
    instead. Thus, the following procedure for determining whether D == 0 will
    eventually terminate:
    
    - if the number of terms n is 0, return True
    - if the number of terms n is 1, return c_1 == 0
    - if there is a r_{i,j} common to each summand, factor it out
    - pick one of the r_{i,j}, split the sum into two parts "left",
      respectively, "right" of all the terms containing sqrt(r_{i,j}),
      respectively, not containing sqrt(r_{i,j}).
    - If left^2 - right^2 == 0 is False, return False.
      (sqrt(r_{i,j})^2 simplifies to r_{i,j} and disappears, so the resulting
      expression is easier and this recursion terminates eventually.)
    - If left == 0 (some comment applies), return True
    - Use interval arithmetic of increasing precision until it is high enough
      to determine the signs of left and right.
      Return True if and only if the signs differ, otherwise False.

    Examples::

        sage: from sage.rings.number_field.number_field import NumberField
        sage: from sage.rings.integer import Integer
        sage: from sage.rings.rational import Rational
        sage: from sage.rings.real_mpfr import RealLiteral, RealField
        sage: from sage.rings.real_mpfi import RealIntervalField
        sage: from sage.calculus.var import var
        sage: from sage.functions.other import sqrt
        sage: x = var('x')
        sage: poly = x ** 6 + Rational((3,2))*x**4 + Rational((9,16))*x**2 - Rational((23,64))
        sage: nf = NumberField(poly, 'z', embedding = RealField()(0.56227951206))
        sage: z = nf.gen()

        sage: A = SqrtLinCombination(z)
        sage: B = SqrtLinCombination(Rational((8,9))*z**4 + Rational((10,9))*z**2 + Rational((2,9)))
        sage: C = SqrtLinCombination(3)
        sage: D = SqrtLinCombination(Integer(5))
        sage: E = SqrtLinCombination(Rational((6,7)))

        sage: A + B
        (8/9*z^4 + 10/9*z^2 + z + 2/9) * sqrt(1)
        sage: B - E
        (8/9*z^4 + 10/9*z^2 - 40/63) * sqrt(1)
        sage: A + sqrt(B)
        (1) * sqrt(8/9*z^4 + 10/9*z^2 + 2/9)+(z) * sqrt(1)
        sage: A + sqrt(B) * sqrt(B)
        (8/9*z^4 + 10/9*z^2 + z + 2/9) * sqrt(1)
        sage: A + sqrt(B) * sqrt(B) + C == A + B + C
        True
        sage: A / E
        (7/6*z) * sqrt(1)
        sage: B / A.sqrt()
        (128/207*z^5 + 376/207*z^3 + 302/207*z) * sqrt(z)
        sage: B / (D * A.sqrt())
        (128/1035*z^5 + 376/1035*z^3 + 302/1035*z) * sqrt(z)
        sage: RIF = RealIntervalField(100)
        sage: RIF(B.sqrt() + E.sqrt())
        1.73967449622339881238507307209?
        sage: A - B == 0
        False
        sage: A.sqrt() + B.sqrt() 
        (1) * sqrt(8/9*z^4 + 10/9*z^2 + 2/9)+(1) * sqrt(z)
        sage: 3 * A.sqrt() + (4 * B).sqrt() + C + 8 == (9 * A).sqrt() + 2 * B.sqrt() + (C * C).sqrt() + 11 - 3
        True

    """

    def __init__(self, value = None, d = {}, embed_cache = None):
        # Initialize from either a value or a dictionary
        
        #    c_1 * sqrt(r_1) + c_2 * sqrt(r_2) + ... + c_n * sqrt(r_n)
        #
        # is encoded as dictionary
        #
        #   { r_1 : c_1, r_2 : c_2, ..., r_n : c_n }


        if not value is None:
            if d:
                raise TypeError("SqrtLinCombination has both value and "
                                "dictionary.")

            # Write value as
            #    value * sqrt(1)
            #
            # Use empty dictionary when value is zero.

            self._dict = _filter_zero(
                { _One : _convert_to_allowed_type(value) })
        else:
            # Filter out zero elements
            self._dict = _filter_zero(d)
            
        # Set embed cache, see _get_interval_embedding_from_cache for details
        self._embed_cache = embed_cache

    def __add__(self, other):
        # Try to convert other term to SqrtLinCombination if necessary
        if not isinstance(other, SqrtLinCombination):
            return self + SqrtLinCombination(
                other, embed_cache = _get_embed_cache(self, other))

        # Add
        d = {}
        for k, v in self._dict.items():
            d[k] = d.get(k, 0) + v
        for k, v in other._dict.items():
            d[k] = d.get(k, 0) + v
        return SqrtLinCombination(
            d = d,
            embed_cache = _get_embed_cache(self, other))

    def __neg__(self):
        # Negate
        return SqrtLinCombination(
            d = dict( (k, -v) for k, v in self._dict.items() ),
            embed_cache = self._embed_cache)

    def __sub__(self, other):
        # Subtract
        return self + (-other)

    def __mul__(self, other):
        # Try to convert other term to SqrtLinCombination if necessary
        if not isinstance(other, SqrtLinCombination):
            return self * SqrtLinCombination(
                other,
                embed_cache = _get_embed_cache(self, other))

        # Result
        d = {}

        # Multiply each term with each term
        for k1, v1 in self._dict.items():
            for k2, v2 in other._dict.items():
                # multiply c_i * sqrt(r_i) * c_j * sqrt(r_j)

                # c_i * c_j
                p = v1 * v2

                # Multiplying the two roots sqrt(r_i) sqrt(r_j)
                if k1 == k2:
                    # Case r_i = r_j
                    # The term becomes (r_i * c_i * c_j) * sqrt(1)
                    d[_One] = d.get(_One, 0) + k1 * p
                else:
                    # Case r_i != r_j
                    # The term becomes (c_i * c_j) * sqrt(r_i * r_j)
                    m = k1 * k2
                    d[m] = d.get(m, 0) + p
        return SqrtLinCombination(
            d = d, embed_cache = _get_embed_cache(self, other))

    def inverse(self):
        # The inverse element of                c_1 * sqrt(r_1)
        #                     is  (1 / (c_1 * r_1)) * sqrt(r_1)
        l = len(self._dict)
        if not l == 1:
            # Do not implement other elements.
            if l == 0:
                # In particular, do not invert 0
                raise ZeroDivisionError('SqrtLinCombination division by zero')
            raise TypeError('SqrtLinCombination division not fully '
                            'implemented')

        # Iteration over the only term
        for k, v in self._dict.items():
            return SqrtLinCombination( 
                d = { k : 1 / (v * k) },
                embed_cache = self._embed_cache)

    def __div__(self, other):
        # Try to convert other term to SqrtLinCombination if necessary
        if not isinstance(other, SqrtLinCombination):
            return self / SqrtLinCombination(
                other, embed_cache = _get_embed_cache(self, other))
        return self * other.inverse()

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return (-self) + other

    def __rmul__(self, other):
        return self * other

    def __rdiv__(self, other):
        return self.inverse() * other

    def sqrt(self):
        # Implent sqrt of 0 and c_1 * sqrt(1)
        l = len(self._dict)
        if l == 0:
            # sqrt of 0
            return SqrtLinCombination(
                embed_cache = self._embed_cache)
        if l == 1:
            # Iterate through only term
            for k, v in self._dict.items():
                # Make sure expression in sqrt is 1
                if not k == 1:
                    raise TypeError('SqrtLinCombination sqrt not fully '
                                    'implemented')
                return SqrtLinCombination(
                    d = { v: _One},
                    embed_cache = self._embed_cache)
        raise TypeError('SqrtLinCombination sqrt not fully implemented')

    def __repr__(self):
        if self._dict:
            return '+'.join(
                ['(%r) * sqrt(%r)' % (v, k) for k, v in self._dict.items()])
        return '0'

    def __eq__(self, other):
        """
        Implements the == operator as described above.
        """
        diff = self - other

        # Convert to type holding linear combinations of factorized
        # sqrts.
        f = _FactorizedSqrtLinCombination.from_sqrt_lin_combination(diff)
        return f.is_zero()

    def __lt__(self, other):
        raise Exception('Not implemented')

    def __le__(self, other):
        raise Exception('Not implemented')

    def __gt__(self, other):
        raise Exception('Not implemented')

    def __ge__(self, other):
        raise Exception('Not implemented')
        

    def _real_mpfi_(self, RIF):
        """
        Convert to interval in given RealIntervalField instance.
        """

        def eval_term(k, v):
            # Evaluate one term c_i * sqrt(r_i)
            # where c_i = k, r_i = v
            s = _to_RIF(k, RIF, self._embed_cache)
            if not s > 0:
                raise _SqrtException()
            return _to_RIF(v, RIF, self._embed_cache) * s.sqrt()

        # Sum over all terms
        return sum([eval_term(k, v) for k, v in self._dict.items()], RIF(0))

    def _sign_numerical(self, prec):
        """
        Use interval arithmetics with precision prec to try to determine the
        sign. If we could not certify the sign, return None.
        The result is a pair (sign, interval).
        """

        # Evaluate as interval
        RIF = RealIntervalField(prec)
        try:
            interval_val = RIF(self)
        except _SqrtException:
            # This exception happens if we try to take the square root of an
            # interval that contains negative numbers.
            # This is not supposed to happen but if we take the square of a small
            # number and the precision is low, it might happen.
            # It just means we need to use higher precision.
            # So just return "None" to indicate failed certification.
            return None, None

        # Interval certifies positive sign
        if interval_val > 0:
            return +1, interval_val
        # Interval certified negative sign
        if interval_val < 0:
            return -1, interval_val
        # Interval contains zero and we can't say.
        return None, interval_val

    def sign_with_interval(self):
        """
        Similar to sign, but for the non-zero case, also return the interval
        certifying the sign - useful for debugging.
        """
        # First try to determine the sign using interval arithmetics in twice
        # the double precision. This is for performance: the exact case can
        # be slow so we try numerically first.
        prec = 106
        numerical_sign, interval_val = self._sign_numerical(prec)
        if not numerical_sign is None:
            # We could determine the sign using interval arithmetics
            # Return the result.
            return numerical_sign, interval_val

        # Now try to determine whether it is zero using exact arithmetics.
        if self == 0:
            # It is zero
            return 0, 0

        # We know that the value is non-zero. Increase precision until we have
        # determined the sign using interval arithmetics.
        while True:
            prec *= 2
            numerical_sign, interval_val = self._sign_numerical(prec)
            if not numerical_sign is None:
                return numerical_sign, interval_val

    def sign(self):
        """
        Returns the +1, 0, -1 depending on whether the value is positive,
        zero or negative. For the zero case, exact artihmetic is used to
        certify. Otherwise, interval arithmetic is used.
        
        """
        return self.sign_with_interval()[0]

class ComplexSqrtLinCombination(object):
    """
    A pair (real, imag) of SqrtLinCombinations representing the complex number
    real + imag * I. Supports ``real()``, ``imag()``, ``+``, ``-``, ``*``, ``/``,
    ``abs``, ``conjugate()`` and ``==``.
    """

    def __init__(self, real, imag = 0, embed_cache = None):
        if isinstance(real, SqrtLinCombination):
            self._real = real
        else:
            self._real = SqrtLinCombination(
                real,
                embed_cache = embed_cache)

        if isinstance(imag, SqrtLinCombination):
            self._imag = imag
        else:
            self._imag = SqrtLinCombination(
                imag,
                embed_cache = embed_cache)

    def __repr__(self):
        return "ComplexSqrtLinCombination(%r, %r)" % (self._real, self._imag)

    def real(self):
        """
        Real part.
        """
        return self._real

    def imag(self):
        """
        Imaginary part.
        """
        return self._imag

    def __abs__(self):
        """
        Absolute value.
        """

        return sqrt(self._real * self._real + self._imag * self._imag)

    def __add__(self, other):
        if not isinstance(other, ComplexSqrtLinCombination):
            return self + ComplexSqrtLinCombination(other)
        
        return ComplexSqrtLinCombination(self._real + other._real,
                                         self._imag + other._imag)

    def __neg__(self):
        return ComplexSqrtLinCombination(-self._real, -self._imag)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, ComplexSqrtLinCombination):
            return self * ComplexSqrtLinCombination(other)

        return ComplexSqrtLinCombination(
            self._real * other._real - self._imag * other._imag,
            self._real * other._imag + self._imag * other._real)

    def __div__(self, other):
        if not isinstance(other, ComplexSqrtLinCombination):
            return self / ComplexSqrtLinCombination(other)

        num = 1 / (other._real * other._real + other._imag * other._imag)

        return ComplexSqrtLinCombination(
            (self._real * other._real + self._imag * other._imag) * num,
            (other._real * self._imag - self._real * other._imag) * num)
    
    def conjugate(self):
        return ComplexSqrtLinCombination(self._real, -self._imag)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return (-self) + other

    def __rmul__(self, other):
        return self * other

    def __rdiv__(self, other):
        return ComplexSqrtLinCombination(other) / self

    def __eq__(self, other):
        if not isinstance(other, ComplexSqrtLinCombination):
            return self == ComplexSqrtLinCombination(other)

        return (self._real == other._real) and (self._imag == other._imag)

    def __ne__(self, other):
        return not (self == other)
        
    def __lt__(self, other):
        raise TypeError('No order on complex numbers.')

    def __le__(self, other):
        raise TypeError('No order on complex numbers.')

    def __gt__(self, other):
        raise TypeError('No order on complex numbers.')

    def __ge__(self, other):
        raise TypeError('No order on complex numbers.')

    def _complex_mpfi_(self, CIF):
        """
        Convert to complex interval in given ComplexIntervalField instance.
        """

        # Get corresponding RealIntervalField
        RIF = CIF(0).real().parent()
        # And just pair
        return CIF(RIF(self._real), RIF(self._imag))

class _SqrtException(Exception):
    pass

class _FactorizedSqrtLinCombination(object):
    def __init__(self, d = {}, embed_cache = None):
        #       c_1 * sqrt(r_{1,1}) * sqrt(r_{1,2}) * ... * sqrt(r_{1,k_1})
        #     + c_2 * sqrt(r_{2,1}) * sqrt(r_{2,2}) * ... * sqrt(r_{2,k_2})
        #     + ...
        #     + c_n * sqrt(r_{n,1}) * sqrt(r_{n,2}) * ... * sqrt(r_{n,k_n})
        #
        # is encoded by a dictionary
        #
        # { frozenset([r_{1,1}, r_{1,2}, ..., r_{1,k_1}]) : c_1,
        #   frozenset([r_{2,1}, r_{2,2}, ..., r_{2,k_2}]) : c_2,
        #   ...,
        #   frozenset([r_{n,1}, r_{n,2}, ..., r_{n,k_n}]) : c_n }

        self._dict = _filter_zero(d)

        # Set embed cache, see _get_interval_embedding_from_cache for details
        self._embed_cache = embed_cache

    def _real_mpfi_(self, RIF):

        def eval_term(k, v):
            # Evaluate one term 
            # c_i * sqrt(r_{i,1}) * sqrt(r_{i,2}) * ... * sqrt(r_{i,k_2})
            # where c_i is stored in v
            # and k is the set of r_{i,j}
            
            # Take the product of all r_{i,j} after converting to intervals
            prod = reduce(
                operator.mul,
                [_to_RIF(t, RIF, self._embed_cache) for t in k],
                RIF(1))

            # Raise exception if interval isn't positive
            if not prod > 0:
                raise _SqrtException()

            # Return interval for term
            return prod.sqrt() * _to_RIF(v, RIF, self._embed_cache)

        # Sum over all terms
        return sum([eval_term(k, v) for k, v in self._dict.items()], RIF(0))

    def __repr__(self):
        if not self._dict:
            return '0'

        def term(item):
            k, v = item
            b = '(%r)' % v
            for s in k:
                b += ' * sqrt(%r)' % s
            return b

        return '+'.join([term(item) for item in self._dict.items()])

    @staticmethod
    def from_sqrt_lin_combination(l):
        """
        Construct from a SqrtLinCombination.
        """

        # Need to change encoding, see __init__
        def to_set(k):
            if k == _One:
                return frozenset()
            else:
                return frozenset([k])

        return _FactorizedSqrtLinCombination(dict(
            (to_set(k), v) for k, v in l._dict.items()),
            embed_cache = l._embed_cache)

    def __add__(self, other):
        # Add
        d = {}
        for k, v in self._dict.items():
            d[k] = d.get(k, 0) + v
        for k, v in other._dict.items():
            d[k] = d.get(k, 0) + v
        return _FactorizedSqrtLinCombination(
            d,
            embed_cache = _get_embed_cache(self, other))

    def __neg__(self):
        return _FactorizedSqrtLinCombination(
            dict((k, -v) for k, v in self._dict.items()),
            embed_cache = self._embed_cache)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        d = {}
        # Multiply each term with each
        for k1, v1 in self._dict.items():
            for k2, v2 in other._dict.items():
                # Multiply
                # c_i * sqrt(r_{i,1}) * ... * sqrt(r_{i,k_i})
                # with
                # c'_i' * sqrt(r'_{i',1}) * ... * sqrt(r'_{i',k'_i'})
                #
                # If sqrt(r) appears in both terms, it becomes
                # sqrt(r) * sqrt(r) = r and is multiplied into the coefficient
                # (this is done by _prod(k1 & k2)).
                # A sqrt(r) appearing only appearing in one term survives
                # (k1^k2)

                k = k1 ^ k2
                v = v1 * v2 * _prod(k1 & k2)
                d[k] = d.get(k, 0) + v
        return _FactorizedSqrtLinCombination(
            d, embed_cache = _get_embed_cache(self, other))

    def is_zero(self):
        """
        Returns True if it is zero, False otherwise.
        """

        # Implements the algorithm for operator == described in 
        # SqrtLinCombination

        # The case of no terms n = 0
        if not self._dict:
            return True

        # Case of one term n = 1
        if len(self._dict) == 1:
            return _first(self._dict.values()) == 0

        # Find all r_{i,j} common to all summands
        common_terms = reduce(
            operator.and_, self._dict.keys())

        # Factor them out
        d = dict((k - common_terms, v) for k, v in self._dict.items())

        # Pick one r_{i,j}
        term = _firstfirst(d.keys())
        
        # Split the summands into "left" and "right"
        left = _FactorizedSqrtLinCombination(
            dict( (k, v) for k, v in d.items() if term in k ),
            embed_cache = self._embed_cache)
        right = _FactorizedSqrtLinCombination(
            dict( (k, v) for k, v in d.items() if not term in k),
            embed_cache = self._embed_cache)

        # Check left^2 - right^2 == 0
        if not (left * left - right * right).is_zero():
            return False

        # Check left == 0
        if left.is_zero():
            return True

        # Start with double precision and then increase until we could
        # determine the signs of left and right
        prec = 53
        while True:
            # Determine signs, None indicates the signs couldn't be certified
            opposite_signs = _opposite_signs(left, right, prec)
            if not opposite_signs is None:
                # Done
                return opposite_signs
            
            # Otherwise, increase precision
            prec *= 2


def _opposite_signs(left, right, prec):
    """
    Given two objects left and right that can be coerced to real interval of
    the given precision, try to certify their signs. If succeed, return True
    if the signs are opposite and False otherwise. If failed, return None.
    """

    # Try to cast the elements to real intervals
    RIF = RealIntervalField(prec)
    try:
        left_interval = RIF(left)
        right_interval = RIF(right)
    except _SqrtException:
        # This exception happens if we try to take the square root of an
        # interval that contains negative numbers.
        # This is not supposed to happen but if we take the square of a small
        # number and the precision is low, it might happen.
        # It just means we need to use higher precision.
        # So just return "None" to indicate failed certification.
        return None
    
    # Try to determine sign of left expression.
    left_negative    = bool(left_interval  < 0)
    left_positive    = bool(left_interval  > 0)
    left_determined  = left_negative  or left_positive
    
    # Try to determine sign of right expression
    right_negative   = bool(right_interval < 0)
    right_positive   = bool(right_interval > 0)
    right_determined = right_negative or right_positive
    
    # If both signs could be determined
    if left_determined and right_determined:
        # Return true if and only if signs are opposite
        return left_positive ^ right_positive
    
    # At least one sign couldn't be determined.
    return None

def _first(iterable):
    """
    Return first element of iterable.
    """
    for i in iterable:
        return i

def _firstfirst(iterable):
    """
    Given a nested iterable, i.e., list of lists, return the first element
    of the first non-empty element.
    """
    for i in iterable:
        for j in i:
            return j

def _prod(s):
    """
    The product of the elements in s. Returns Sage Integer(1)
    when s is empty.
    """
    return reduce(operator.mul, s, _One)

def _filter_zero(d):
    """
    Given a dict, filter out all items where the value is 0.
    """

    return dict( (k, v) for k, v in d.items() if not v == 0)
 
def _convert_to_allowed_type(number):
    """
    When given a Python int, convert to Sage Integer (so that
    division of two integers gives a Rational). Otherwise,
    check that the type is allowed.
    """

    if isinstance(number, int):
        return Integer(number)
    if isinstance(number, Integer):
        return number
    if isinstance(number, Rational):
        return number
    if isinstance(number, NumberFieldElement):
        return number

    raise Exception("Not an allowed type")

def _get_embed_cache(l1, l2):
    """
    Given objects of type SqrtLinCombination or _FactorizedSqrtLinCombination
    return the first _embed_cache that is not None.
    For example, one SqrtLinCombination might be instantiated from an
    Integer and the other from an element in the number field that we are
    currently working in. Then only the latter one has an _embed_cache. Thus,
    the need for this function when adding, multiplying, ... those two
    instances.
    """
    for l in [l1, l2]:
        if ((isinstance(l, SqrtLinCombination) or
             isinstance(l, _FactorizedSqrtLinCombination)) and
            not l._embed_cache is None):
            return l._embed_cache
        
    return None

def _get_interval_embedding_from_cache(nf, RIF, cache):
    """
    Evaluate RIF(nf.gen_embedding()) where RIF is a RealIntervalField with
    some precision. This is a real interval that is guarenteed to contain the
    prefered root of the defining polynomial of the number field.

    To avoid re-evaluation, use cache which is (a reference) to a python
    dictionary.

    The idea is that while working over one number field, all instances of
    (_Factorized)SqrtLinCombination have a reference to the same (shared) python
    dictionary and fill it in as needed.

    Unfortunately, the reference to the cache needs to passed down along a lot
    of places. There might be a nicer mechanism for doing this.
    """

    # Cache is None (vs an empty dictionary) means that we do not wish to use
    # a cache.

    # Uncomment to debug performance problems that are suspected to come
    # from the reference to the cache not being passed along
    # if cache is None:
    #     print("Warning: No cache used")

    # The key 'gen_embedding' holds the value of nf.gen_embedding()
    if (not cache is None) and 'gen_embedding' in cache:
        # We can read it from cache
        gen_embedding = cache['gen_embedding']
    else:
        # We need to evaluate it
        gen_embedding = nf.gen_embedding()
        if (not cache is None):
            # Save in cache for future use
            cache['gen_embedding'] = gen_embedding

    # Get the desired precision of the RealIntervalField
    prec = RIF.prec()
    # The precision (which is an int) is the key into the cache
    if (not cache is None) and prec in cache:
        # RIF(nf.gen_embedding()) is in the cache
        # We can just return the result
        return cache[prec]
    
    # We need to actually compute it.
    interval = RIF(gen_embedding)
    if not cache is None:
        # Save in cache for future use.
        cache[prec] = interval

    return interval

def _to_RIF(x, RIF, embed_cache = None):
    """
    Given a Sage Integer, Rational or an element x in a
    Sage NumberField with a real embedding and an instance
    of a RealIntervalField to specify the desired precision,
    return a real interval containing the true value of x.

    Warning: one can actually call RIF(x) and get an interval, but I have
    found examples where that interval does not contain the true value!
    Seems a bug in Sage. CIF(x) doesn't work, so maybe there is just some
    sequence of casts going on to convert x to an interval that wasn't
    anticipated.
    """
    # Handle Integer and Rational case
    if isinstance(x, Integer) or isinstance(x, Rational):
        return RIF(x)

    # Get the number field
    nf = x.parent()

    # Get the generator of number field as interval
    # The code is equivalent to root = RIF(nf.gen_embedding()) but
    # caches the result.
    root = _get_interval_embedding_from_cache(nf, RIF, embed_cache)

    # Sanity check on the root. The polynomial should be
    # zero at it, so the interval has to contain zero.
    # This does not certify it. To certify, we would need
    # to take each end point of the interval, evaluate
    # it using interval arithmetics and check for opposite
    # signs
    if not nf.defining_polynomial()(root).contains_zero():
        raise Exception("Root failed test.")

    # Evaluate the polynomial representing the element in the number field
    # at the root
    return x.lift()(root)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
