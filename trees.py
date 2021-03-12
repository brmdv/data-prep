"""Preprocess NYC Trees dataset. An exact walkthrough can be found in the accompanying Notebook file.

Usage:
    python trees.py INPUTFILE OUTPUTFILE
"""

import pandas as pd
from sys import argv

if __name__ == "__main__":
    if len(argv) != 3:
        print(__doc__)
    else:
        # Read data
        df = pd.read_csv(
            argv[1], parse_dates=[[0, 1]], dtype={"zip_code": pd.UInt16Dtype()}
        )

        # import data
        df = pd.read_csv(argv[1], parse_dates=[0])
        df.set_index("tree_id", inplace=True)

        # replace long and lat with data from the_geom
        df["longitude"] = (
            df["the_geom"].apply(lambda x: x[7:-1].split(" ")[0]).astype("float64")
        )
        df["latitude"] = (
            df["the_geom"].apply(lambda x: x[7:-1].split(" ")[1]).astype("float64")
        )

        # drop redundant columns
        df.drop(["the_geom", "state", "x_sp", "y_sp"], axis=1, inplace=True)

        # Change yes/no values to 1/0
        df.loc[:, "root_stone":"brnch_othe"] = df.loc[
            :, "root_stone":"brnch_othe"
        ].replace(to_replace=["No", "Yes"], value=[0, 1])

        # write output file
        df.to_csv(argv[2])
