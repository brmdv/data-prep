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

        # Change yes/no values to 1/0
        df.loc[:, "root_stone":"brnch_othe"] = df.loc[
            :, "root_stone":"brnch_othe"
        ].replace(to_replace=["No", "Yes"], value=[0, 1])

        # consolidate option columns
        df["curb_loc"].replace(["OnCurb", "OffsetCurb"], [1, 0], inplace=True)
        df["sidewalk"].replace(["Damage", "NoDamage"], [1, 0], inplace=True)
        df.rename(
            columns={"curb_loc": "is_OnCurb", "sidewalk": "sidewalk_damaged"},
            inplace=True,
        )

        status = pd.get_dummies(df["status"], drop_first=True)
        df["is_dead"] = status.iloc[:, 0]
        df["is_stump"] = status.iloc[:, 1]

        df["health"].replace(["Good", "Fair", "Poor"], [2, 1, 0], inplace=True)

        df["steward"].replace(
            ["None", "1or2", "3or4", "4orMore"], [0, 1, 3, 4], inplace=True
        )

        # drop redundant columns
        df.drop(
            ["the_geom", "spc_latin", "state", "x_sp", "y_sp", "status"],
            axis=1,
            inplace=True,
        )

        # write output file
        df.to_csv(argv[2])
