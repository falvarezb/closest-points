import hypothesis.strategies as st
from hypothesis import given, settings, note
import pytest
from quadratic_sol import quadratic_solution
from nlogn_sol import nlogn_solution
from multiproc_sol import nlogn_solution_multiproc
from util import *


@pytest.fixture
def split_even_number_points_fixture():
    p1, p2, p3, p4 = (0, 0), (1, 4), (2, 5), (3, 4)
    Px = [p1, p2, p3, p4]
    Py = [PyElement(p1, 0), PyElement(p2, 1), PyElement(p3, 2), PyElement(p4, 3)]
    return (p1, p2, p3, p4), Px, Py


@pytest.fixture
def split_odd_number_points_fixture():
    p1, p2, p3, p4, p5 = (0, 0), (1, 4), (2, 5), (3, 4), (4, 0)
    Px = [p1, p2, p3, p4, p5]
    Py = [PyElement(p1, 0), PyElement(p2, 1), PyElement(p3, 2), PyElement(p4, 3), PyElement(p5, 4)]
    return (p1, p2, p3, p4, p5), Px, Py


def test_quadratic_solution():
    P = [Point(0, 1), Point(0, 3), Point(2, 0), Point(0, 0)]
    assert quadratic_solution(P) == PointDistance(Point(0, 1), Point(0, 0), 1)


def test_nlogn_left_half_solution():
    P = [Point(3, 9), Point(1, 5), Point(0, 1), Point(5, 3), Point(8, 6), Point(20, 20), Point(40, 40)]
    assert nlogn_solution(P) == PointDistance(Point(0, 1), Point(1, 5), 4.123105625617661)


def test_nlogn_right_half_solution():
    P = [Point(3, 9), Point(1, 5), Point(0, 1), Point(5, 3), Point(8, 6), Point(20, 20), Point(20, 21)]
    assert nlogn_solution(P) == PointDistance(Point(20, 20), Point(20, 21), 1)


def test_nlogn_inter_halves_solution():
    P = [Point(2, -100), Point(0, 0), Point(8, 100), Point(10, 0), Point(12, 100), Point(20, -100), Point(20, 0)]
    assert nlogn_solution(P) == PointDistance(Point(8, 100), Point(12, 100), 4)

def test_nlogn_inter_halves_solution_two_solutions():
    '''
    Possible solutions:
    1. (8,100),(12,100)
    2. (9,70),(13,70)
    Solution corresponding to the point with the lowest coordinate y is selected
    '''
    P = [Point(2, -100), Point(0, 0), Point(8, 100), Point(10, 0), Point(12, 100), Point(20, -100), Point(20, 0), Point(9, 70), Point(13, 70)]
    assert nlogn_solution(P) == PointDistance(Point(9, 70), Point(13, 70), 4)


def test_nlogn_repeat_points():
    P = [Point(3, 9), Point(1, 5), Point(10, 5), Point(3, 9)]
    assert nlogn_solution(P) == PointDistance(Point(3, 9), Point(3, 9), 0)


def test_nlogn_solution_par():
    P = [Point(0, 1), Point(0, 3), Point(2, 0), Point(0, 0)]
    assert nlogn_solution_multiproc(P, 1) == PointDistance(Point(0, 0), Point(0, 1), 1)


def test_sort_points():
    P = [Point(0, 0), Point(3, 4), Point(2, 5), Point(1, 4)]
    Px, Py = sort_points(P)
    assert Px == [Point(0, 0), Point(1, 4), Point(2, 5), Point(3, 4)]
    assert Py == [PyElement(Point(0, 0), 0), PyElement(Point(1, 4), 1),
                  PyElement(Point(3, 4), 3), PyElement(Point(2, 5), 2)]


def test_left_half_even(split_even_number_points_fixture):
    (p1, p2, p3, p4), Px, Py = split_even_number_points_fixture
    newPx, newPy = left_half_points(Px, Py)
    assert newPx == [p1, p2]
    assert newPy == [PyElement(p1, 0), PyElement(p2, 1)]


def test_right_half_even(split_even_number_points_fixture):
    (p1, p2, p3, p4), Px, Py = split_even_number_points_fixture
    newPx, newPy = right_half_points(Px, Py)
    assert newPx == [p3, p4]
    assert newPy == [PyElement(p3, 0), PyElement(p4, 1)]


def test_left_half_odd(split_odd_number_points_fixture):
    (p1, p2, p3, p4, p5), Px, Py = split_odd_number_points_fixture
    newPx, newPy = left_half_points(Px, Py)
    assert newPx == [p1, p2, p3]
    assert newPy == [PyElement(p1, 0), PyElement(p2, 1), PyElement(p3, 2)]


def test_right_half_odd(split_odd_number_points_fixture):
    (p1, p2, p3, p4, p5), Px, Py = split_odd_number_points_fixture
    newPx, newPy = right_half_points(Px, Py)
    assert newPx == [p3, p4, p5]
    assert newPy == [PyElement(p3, 0), PyElement(p4, 1), PyElement(p5, 2)]


def test_quadratic_solution_unstable():
    '''
    solution depends on the original order of the points
    '''
    assert quadratic_solution([Point(0, 0), Point(0, 1), Point(1, 0)]) == PointDistance(Point(0, 0), Point(0, 1), 1)
    assert quadratic_solution([Point(0, 0), Point(1, 0), Point(0, 1)]) == PointDistance(Point(0, 0), Point(1, 0), 1)


def test_nlogn_solution_stable():
    '''
    solution does not depend on the original order of the points
    '''
    assert nlogn_solution([Point(0, 0), Point(0, 1), Point(1, 0)]) == PointDistance(Point(0, 0), Point(0, 1), 1)
    assert nlogn_solution([Point(0, 0), Point(1, 0), Point(0, 1)]) == PointDistance(Point(0, 0), Point(0, 1), 1)


def point_strategy(x, y):
    return Point(x, y)


@given(st.lists(st.builds(point_strategy, st.integers(0, 1000), st.integers(0, 1000)), min_size=2, max_size=100, unique=True))
def test_quadratic_vs_nlogn(P):
    # we cannot compare solutions directly (but just distances) as quadratic solutions are not stable
    assert quadratic_solution(P).d == nlogn_solution(P).d


@settings(max_examples=100, deadline=None)
@given(st.lists(st.builds(point_strategy, st.integers(0, 10000), st.integers(0, 10000)), min_size=2, max_size=100, unique=True))
def test_nlogn_vs_nlogn_par(P):
    par_sol = nlogn_solution_multiproc(P, 4)
    seq_sol = nlogn_solution(P)
    note(f"par_sol={par_sol}")
    note(f"seq_sol={seq_sol}")
    assert par_sol == seq_sol
