import numpy as np
def get_angle(inp, cross, k, direction):
    # inp is the input plane, represented by 3 xzy sets
    # cross and k is the normal vector of the plane
    # Direction defines whether we want the mediolateral or dorsaventral angle
    section = inp.copy()
    # transform vector into absolute coordinates
    for i in range(3):
        section[i + 3] += section[i]
        section[i + 6] += section[i]
    if direction == "ML":
        # original xzy point
        a = section[0:2]
        # calculate a point which differs from this point only in the x dimension
        # to do this we use the plane equation which tells us the position of every point on the plane
        linear_point = (((section[0] - 100) * cross[0]) + ((section[2]) * cross[2])) + k
        # this tells us the depth of that point which differs in x dimension but lies on the same plane
        depth = -(linear_point / cross[1])
        b = np.array((section[0] - 100, depth))
        c = b + [100, 0]

    if direction == "DV":
        a = section[1:3]
        linear_point = (((section[0]) * cross[0]) + ((section[2] - 100) * cross[2])) + k
        depth = -(linear_point / cross[1])
        b = np.array((depth, section[2] - 100))
        c = b + [0, 100]
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    # This looks redundant, needs to be tested
    angle = np.arccos(cosine_angle)
    angle = np.degrees(angle)
    if direction == "ML":
        if b[1] > a[1]:
            angle *= -1
    if direction == "DV":
        if b[0] < a[0]:
            angle *= -1
    return angle

def calculate_angles(df):
    """
    Calculates the Mediolateral and Dorsoventral angles for a series of predictions
    
    :param df: The dataframe containing the predictions
    :type df: pandas.DataFrame
    :return: a list of calculated ML and DV angles
    :rtype: list[float], list[float]
    """
    DV_list, ML_list = [], []
    for alignment in df.iterrows():
        # the quickNII coordinate vector
        m = alignment[1][
            ["ox", "oy", "oz", "ux", "uy", "uz", "vx", "vy", "vz"]
        ].values.astype(np.float64)
        cross, k = find_plane_equation(m)
        # calculate the Mediolateral and Dorsoventral angles
        DV = get_angle(m, cross, k, "DV")
        ML = get_angle(m, cross, k, "ML")
        # add the angles to the dataframe as new columns
        DV_list.append(DV)
        ML_list.append(ML)
    return DV_list, ML_list

def find_plane_equation(plane):
    """
    Finds the plane equation of a plane
    :param plane: the plane to find the equation of
    :type plane: :any:`numpy.ndarray`
    :returns: the normal vector of the plane and the constant k
    :rtype: :any:`numpy.ndarray`, float
    """
    a, b, c = (
        np.array(plane[0:3], dtype=np.float64),
        np.array(plane[3:6], dtype=np.float64),
        np.array(plane[6:9], dtype=np.float64),
    )
    cross = np.cross(b, c)
    cross /= 9
    k = -((a[0] * cross[0]) + (a[1] * cross[1]) + (a[2] * cross[2]))
    return (cross, k)
