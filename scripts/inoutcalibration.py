from collections import defaultdict

import math


class TripInTripOutMatrix(defaultdict):
    def __init__(self, dim):
        if not dim > 0:
            raise ValueError("dimension must be > 0, but is {}".format(dim))
        self.default_factory = lambda: 0.0
        self.n = dim

    def __setitem__(self, key, value):
        if not isinstance(key, tuple) or len(key) != 2:
            raise KeyError("key must be a pair: {}".format(key))
        if not 1 <= key[0] <= self.n:
            raise KeyError("first index of {} must be between 1 and {}".format(key, self.n))
        if not key[0] <= key[1] <= self.n:
            raise KeyError("second index of {} must be between first index + 1 and {}".format(key, self.n))
        if not isinstance(value, (float, int)):
            raise ValueError("value must be float or int: {}".format(value))
        super(TripInTripOutMatrix, self).__setitem__(key, value)

    def __add__(self, other):
        check_compatibility_of_tripintripout_matrices(self, other)
        new_matrix = TripInTripOutMatrix(self.n)
        keys = self.get_nonzero_entries().union(other.get_nonzero_entries())
        for key in keys:
            new_matrix[key] = self[key] + other[key]
        return new_matrix

    def __mul__(self, other):
        check_compatibility_of_tripintripout_matrices(self, other)
        new_matrix = TripInTripOutMatrix(self.n)
        keys = self.get_nonzero_entries().intersection(other.get_nonzero_entries())
        for key in keys:
            new_matrix[key] = self[key] * other[key]
        return new_matrix

    def __repr__(self):
        res = ""
        for i in range(1, self.n + 1):
            res += " ".join(
                [" " * 10 for j in range(1, i)] + ["{:10.4f}".format(self[i, j]) for j in range(i, self.n + 1)]) + "\n"
        return res

    def mult_by_scalar(self, scalar):
        new_matrix = TripInTripOutMatrix(self.n)
        for key in self.get_nonzero_entries():
            new_matrix[key] = scalar * self[key]
        return new_matrix

    def scalar_product(self, other):
        new_matrix = self * other
        sum = 0.0
        for key in new_matrix.get_nonzero_entries():
            sum += new_matrix[key]
        return sum

    def norm(self):
        return math.sqrt(self.scalar_product(self))

    def get_nonzero_entries(self):
        return {key for key in self.keys() if self[key] != 0.0}

    def get_section_volume(self, k):
        if not 1 <= self.n - 1:
            raise ValueError("index of abschnitt is {}, should be between 1 and {} - 1".format(k, self.n))
        sum = 0.0
        for i in range(1, k + 1):
            for j in range(k + 1, self.n + 1):
                sum += self[i, j]
        return sum

    def get_section_volumes(self):
        return [self.get_section_volume(k) for k in range(1, self.n)]

    def calibrate(self, calibration_volumes):
        b = get_trivial_solution(self.n, calibration_volumes)
        orthonormal_basis_of_normal_space = get_orthonormal_basis_of_normal_space(self.n)
        b_1, b_2 = get_components(b, orthonormal_basis_of_normal_space)
        f_1, f_2 = get_components(self, orthonormal_basis_of_normal_space)
        s = b_2.scalar_product(f_2) / f_2.norm() ** 2
        return b_2 + f_1.mult_by_scalar(s)


def get_components(tripintripout_matrix, orthonormal_basis):
    v_2 = TripInTripOutMatrix(tripintripout_matrix.n)
    for i in range(len(orthonormal_basis)):
        orthonormal_matrix = orthonormal_basis[i]
        v_2 += orthonormal_matrix.mult_by_scalar(tripintripout_matrix.scalar_product(orthonormal_matrix))
    v_1 = tripintripout_matrix + v_2.mult_by_scalar(-1.0)
    return v_1, v_2


def get_trivial_solution(dim, section_volumes):
    if len(section_volumes) != dim - 1:
        raise ValueError("section volumes must have length {}, but have length {}".format(dim - 1, len(
            section_volumes)))
    trivial_solution = TripInTripOutMatrix(dim)
    for i in range(0, dim - 1):
        trivial_solution[i + 1, i + 2] = section_volumes[i]
    return trivial_solution


def check_compatibility_of_tripintripout_matrices(matrix_1, matrix_2):
    if not isinstance(matrix_1, TripInTripOutMatrix):
        raise TypeError("must be a TripInTripOutMatrix-matrix: {}".format(matrix_1))
    if not isinstance(matrix_2, TripInTripOutMatrix):
        raise TypeError("must be a TripInTripOutMatrix-matrix: {}".format(matrix_2))
    if matrix_1.n != matrix_2.n:
        raise ValueError("matrices not of same dimension: {} and {}".format(matrix_1.n, matrix_2.n))
    return True


def create_unit_matrix(i, j, dim):
    if not 1 <= i <= dim or not 1 <= j <= dim:
        raise ValueError("{} and {} bust be between 1 and {}".format(i, j, dim))
    matrix = TripInTripOutMatrix(dim)
    matrix[i, j] = 1
    return matrix


def create_alpha(k_from, k_to, dim):
    if not 1 <= k_from < k_to < dim:
        raise ValueError("1 <= {} <= {} <= {} is violated".format(k_from, k_to, dim))
    matrix = create_unit_matrix(k_from, k_to, dim).mult_by_scalar(-1)
    for i in range(k_from, k_to):
        matrix += create_unit_matrix(i, i + 1, dim)
    return matrix


def create_beta(k, dim):
    matrix = TripInTripOutMatrix(dim)
    for i in range(1, k + 1):
        for j in range(k + 1, dim + 1):
            matrix += create_unit_matrix(i, j, dim)
    return matrix


def get_beta_basis(dim):
    return [create_beta(i, dim) for i in range(1, dim)]


def get_orthonormal_basis_of_normal_space(dim):
    return gram_schmidt(get_beta_basis(dim))


def gram_schmidt(matrices):
    m = len(matrices)
    new_matrices = []
    for i in range(0, m):
        act_matrix = matrices[i]
        for j in range(0, i):
            act_matrix += new_matrices[j].mult_by_scalar(-new_matrices[j].scalar_product(matrices[i]))
        act_matrix = act_matrix.mult_by_scalar(1.0 / act_matrix.norm())
        new_matrices += [act_matrix]
    return new_matrices
