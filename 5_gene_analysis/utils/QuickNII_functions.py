
import pandas as pd
import json
import numpy as np
def read_QUINT_JSON(filename: str) -> pd.DataFrame:
    """
    Converts a QUINT JSON to a pandas dataframe
    
    :param json: The path to the QUINT JSON
    :type json: str
    :return: A pandas dataframe
    :rtype: pd.DataFrame
    """
    with open(filename, "r") as f:
        data = json.load(f)
    sections = data["slices"]
    target_volume = data["target"]
    alignments = [
        row["anchoring"] if "anchoring" in row else 9 * [np.nan] for row in sections
    ]
    height = [row["height"] if "height" in row else [] for row in sections]
    width = [row["width"] if "width" in row else [] for row in sections]
    filenames = [row["filename"] if "filename" in row else [] for row in sections]
    section_numbers = [row["nr"] if "nr" in row else [] for row in sections]
    markers = [row["markers"] if "markers" in row else [] for row in sections]
    df = pd.DataFrame({"Filenames": filenames, "nr": section_numbers})
    df[["ox", "oy", "oz", "ux", "uy", "uz", "vx", "vy", "vz"]] = alignments
    df["markers"] = markers
    df["height"] = height
    df["width"] = width
    return df, target_volume

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