import unittest

from scripts.inoutcalibration import TripInTripOutMatrix, create_alpha, create_beta, get_beta_basis, \
    get_orthonormal_basis_of_normal_space, get_trivial_solution


class TestTripinTripOutCalibration(unittest.TestCase):
    def test_nonzero_entries(self):
        dim = 3
        m_1 = TripInTripOutMatrix(dim)
        m_1[1, 2] = 1.0
        m_1[2, 3] = 5.0
        self.assertEqual(m_1.get_nonzero_entries(), {(1, 2), (2, 3)})

    def test_add(self):
        dim = 3
        m_1 = TripInTripOutMatrix(dim)
        m_1[1, 2] = -1.0
        m_1[1, 3] = 10.0
        m_1[2, 3] = 5.0

        m_2 = TripInTripOutMatrix(dim)
        m_2[1, 2] = 3.0
        m_2[2, 3] = 10.0

        m_add = TripInTripOutMatrix(dim)
        m_add[1, 2] = 2.0
        m_add[1, 3] = 10.0
        m_add[2, 3] = 15.0
        to_test = m_1 + m_2
        self.assertEqual(m_add, to_test, msg="m_add:\n{}\nto_test:\n{}".format(m_add, to_test))

    def test_mult(self):
        dim = 3
        m_1 = TripInTripOutMatrix(dim)
        m_1[1, 2] = -1.0
        m_1[2, 3] = 5.0

        m_2 = TripInTripOutMatrix(dim)
        m_2[1, 2] = 3.0
        m_2[1, 3] = 5.0
        m_2[2, 3] = 10.0

        m_mult = TripInTripOutMatrix(dim)
        m_mult[1, 2] = -3.0
        m_mult[2, 3] = 50.0
        to_test = m_1 * m_2
        self.assertEqual(m_mult, to_test, msg="m_mult:\n{}\nto_test:\n{}".format(m_mult, to_test))

    def test_alpha(self):
        alpha = TripInTripOutMatrix(6)
        alpha[2, 3] = 1.0
        alpha[3, 4] = 1.0
        alpha[4, 5] = 1.0
        alpha[2, 5] = -1.0
        to_test = create_alpha(2, 5, 6)
        self.assertEqual(alpha, to_test, msg="alpha:\n{} \nto_test:\n{}".format(alpha, to_test))

    def test_beta_1(self):
        beta = TripInTripOutMatrix(6)
        beta[1, 4] = 1
        beta[1, 5] = 1
        beta[1, 6] = 1
        beta[2, 4] = 1
        beta[2, 5] = 1
        beta[2, 6] = 1
        beta[3, 4] = 1
        beta[3, 5] = 1
        beta[3, 6] = 1
        to_test = create_beta(3, 6)
        self.assertEqual(beta, to_test, msg="beta:\n{} \nto_test:\n{}".format(beta, to_test))

    def test_beta_2(self):
        beta = TripInTripOutMatrix(3)
        beta[1, 2] = 1
        beta[1, 3] = 1
        to_test = create_beta(1, 3)
        self.assertEqual(beta, to_test, msg="beta:\n{} \nto_test:\n{}".format(beta, to_test))

    def test_scalar_product(self):
        n = 6
        for j in range(1, n):
            for k_from in range(1, n + 1):
                for k_to in range(k_from + 1, n):
                    self.assertEqual(create_alpha(k_from, k_to, n).scalar_product(create_beta(j, n)), 0.0)

    def test_gram_schmidt(self):
        betas = get_beta_basis(5)
        to_test = len(betas)
        should_be = 4
        self.assertEqual(should_be, to_test, msg="should be: {}. is: {}".format(should_be, to_test))

        orthonormal_basis = get_orthonormal_basis_of_normal_space(5)

        for i in range(should_be):
            to_test = orthonormal_basis[i].norm()
            self.assertAlmostEqual(1.0, to_test, places=5,
                                   msg="norm of {}-th matrix is {}, but should be 1.0".format(i, to_test))

        for i in range(should_be):
            matrix_i = orthonormal_basis[i]
            for j in range(i + 1, should_be):
                to_test = matrix_i.scalar_product(orthonormal_basis[j])
                msg = "scalar-product of {}-th and {}-th matrix is {}, should be 0.0".format(i, j, to_test)
                self.assertAlmostEqual(0.0, to_test, places=5, msg=msg)

    def test_get_section_volumes(self):
        dim = 4
        tripintripout_matrix = TripInTripOutMatrix(dim)
        tripintripout_matrix[1, 2] = 3
        tripintripout_matrix[1, 3] = 4
        tripintripout_matrix[1, 4] = 5
        tripintripout_matrix[2, 3] = 6
        tripintripout_matrix[2, 4] = 7
        tripintripout_matrix[3, 4] = 8
        should_be = [12, 22, 20]
        to_test = tripintripout_matrix.get_section_volumes()
        for i in range(dim - 1):
            msg = "volumes on section {}. should be: {}. is: {}".format(i + 1, should_be[i], to_test[i])
            self.assertAlmostEqual(should_be[i], to_test[i], places=5, msg=msg)

    def test_get_trivial_solution(self):
        dim = 4
        section_volumes = [3.0, 4.56, 6.78]
        trivial_solution = get_trivial_solution(dim, section_volumes)
        to_test = trivial_solution.get_section_volumes()
        for i in range(dim - 1):
            msg = "volumes {} on section {} should be reproduces. but is {}".format(
                section_volumes[i], i, to_test[i])
            self.assertAlmostEqual(section_volumes[i], to_test[i], msg=msg)

    def test_calibrate_1(self):
        dim = 4
        tripintripout_matrix = TripInTripOutMatrix(dim)
        tripintripout_matrix[1, 2] = 3
        tripintripout_matrix[1, 3] = 4
        tripintripout_matrix[1, 4] = 5
        tripintripout_matrix[2, 3] = 6
        tripintripout_matrix[2, 4] = 7
        tripintripout_matrix[3, 4] = 8
        calibration_volumes = [10.3, 25.5, 18.3]
        calibrated_tripintripout_matrix = tripintripout_matrix.calibrate(calibration_volumes)
        calibrated_section_volumes = calibrated_tripintripout_matrix.get_section_volumes()
        for i in range(dim - 1):
            should_be = calibration_volumes[i]
            to_test = calibrated_section_volumes[i]
            msg = "calibrated volumes on section {} should equal {}, but is {}".format(i, should_be, to_test)
            self.assertAlmostEqual(should_be, to_test, places=5, msg=msg)

    def test_calibrate_2(self):
        dim = 6
        tripintripout_matrix = TripInTripOutMatrix(dim)
        tripintripout_matrix[1, 2] = 3
        tripintripout_matrix[1, 3] = 4
        tripintripout_matrix[1, 4] = 5
        tripintripout_matrix[2, 3] = 6
        tripintripout_matrix[2, 5] = 7
        tripintripout_matrix[3, 6] = 8
        tripintripout_matrix[4, 5] = 0.4
        tripintripout_matrix[5, 6] = 4
        calibration_volumes = [10.3, 15.0, 25.5, 18.3, 23.0]
        calibrated_tripintripout_matrix = tripintripout_matrix.calibrate(calibration_volumes)
        calibrated_section_volumes = calibrated_tripintripout_matrix.get_section_volumes()
        for i in range(dim - 1):
            should_be = calibration_volumes[i]
            to_test = calibrated_section_volumes[i]
            msg = "calibrated volumes on section {} should equal {}, but is {}".format(i, should_be, to_test)
            self.assertAlmostEqual(should_be, to_test, places=5, msg=msg)


if __name__ == "__main_":
    unittest.main()
