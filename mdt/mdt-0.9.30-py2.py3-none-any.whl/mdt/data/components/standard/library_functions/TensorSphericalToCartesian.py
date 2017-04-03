from mdt.components_config.library_functions import LibraryFunctionConfig
from mot.cl_data_type import SimpleCLDataType
from mot.model_building.cl_functions.parameters import LibraryParameter

__author__ = 'Robbert Harms'
__date__ = "2015-06-21"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class TensorSphericalToCartesian(LibraryFunctionConfig):

    description = '''
        Generates the D matrix for a Tensor compartment.

        The angles ``theta`` and ``phi`` are used for creating the first vector, ``vec0``.
        This vector is then rotated around ``psi`` to generate the first perpendicular orientation, ``vec1``.
        The third vector is generated by being perpendicular to the other two vectors.

        Args:
            theta: polar angle of the first vector
            phi: azimuth angle of the first vector
            psi: rotation around the first vector, used to generate the perpendicular vectors.
    '''
    parameter_list = ['theta', 'phi', 'psi',
                      LibraryParameter(SimpleCLDataType.from_string('mot_float_type4*'), 'vec0'),
                      LibraryParameter(SimpleCLDataType.from_string('mot_float_type4*'), 'vec1'),
                      LibraryParameter(SimpleCLDataType.from_string('mot_float_type4*'), 'vec2')]
    cl_code = '''
        mot_float_type cos_theta;
        mot_float_type sin_theta = sincos(theta, &cos_theta);
        mot_float_type cos_phi;
        mot_float_type sin_phi = sincos(phi, &cos_phi);
        mot_float_type cos_psi;
        mot_float_type sin_psi = sincos(psi, &cos_psi);

        *vec0 = (mot_float_type4)(cos_phi * sin_theta, sin_phi * sin_theta, cos_theta, 0.0);

        // rotate vec0 by 90 degrees, changing, x, y and z
        mot_float_type rotation_factor = sin(theta+(M_PI_2_F));
        *vec1 = (mot_float_type4)(rotation_factor * cos_phi,
                                  rotation_factor * sin_phi,
                                  cos(theta+(M_PI_2_F)),
                                  0.0);

        // uses Rodrigues' formula to rotate vec1 by psi around vec0
        // using a multiplication factor "select(1, -1, (*vec0).z < 0 || (((*vec0).z == 0.0) && (*vec0).x < 0.0))" to
        // prevent commutative problems in the cross product between vec0 x vec1
        *vec1 = *vec1 * cos_psi
                    + (cross(*vec1, select(1, -1, (*vec0).z < 0 ||
                                                   (((*vec0).z == 0.0) && (*vec0).x < 0.0)) * *vec0) * sin_psi)
                    + (*vec0 * dot(*vec0, *vec1) * (1-cos_psi));

        *vec2 = cross(*vec0, *vec1);
    '''
