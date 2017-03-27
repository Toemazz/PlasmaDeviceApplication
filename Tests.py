# Engineer: Thomas Reaney
# College: National University of Ireland Galway
# Date: 09/03/2016
import math


# Method: Used to get the limit for testing
def get_limit(max_dist_between_center_points=25.0):
    """
    :param max_dist_between_center_points: Default maximum allowable distance between ideal center point
                                            and actual center point
    :return: Maximum allowable distance between ideal center point and actual center point
    """
    file = open("limits.txt", "r")

    if file:
        for line in file:
            line = line.split(" ")
            max_dist_between_center_points = float(line[1])
    else:
        print("File not found. Using default limit")
    return max_dist_between_center_points


# Method: Used to check if the test has passed
def check_pass_fail_(point_0, point_1):
    """
    :param point_0: First (x, y) coordinate
    :param point_1: Second (x, y) coordinate
    :return: True if passed, False if failed
    """
    limit = get_limit()
    # Get the distance between the two points
    dist = calc_distance_between_two_points(point_0, point_1)

    # Check if the current run has passed the test
    if dist <= limit:
        return True
    else:
        return False


# Method: Used to calculate the distance between two points
def calc_distance_between_two_points(point0, point1):
    """
    :param point0: Point 0
    :param point1: Point 1
    :return: Distance between the points
    """
    return math.sqrt((point0[0]-point1[0])**2 + (point0[1]-point1[1])**2)
