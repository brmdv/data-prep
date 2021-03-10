"""Preprocess NYC crashed dataset. An exact walkthrough can be found in the accompanying Notebook file.

Usage:
    python crashes.py INPUTFILE OUTPUTFILE
"""

import pandas as pd
from sys import argv


def filter_vehicle(veh) -> str:
    """Simple function to categorize vehicle types 

    :param veh: [description]
    """

    # passthrought NaNs
    if type(veh) != str:
        return veh

    veh = veh.lower()  # lowercase
    # remove spaces and common characters to decrease ambiguity
    veh = veh.replace(" ", "").replace("-", "").replace("/", "")
    # categories
    groups = {
        "large": [
            "truck",
            "uhaul",
            "freight",
            "pickup",
            "bus",
            "ambulance",
            "van",
            "tractor",
            "fire",
            "camper",
        ],
        "normal": ["car", "passenger", "pas", "sedan", "taxi"],
        "two-wheel": ["bicycle", "bike", "motorcycle", "scooter", "vespa"],
    }
    for cat in groups:
        if veh == cat:
            # passthrough if already category
            return veh
        for name in groups[cat]:
            if name in veh:
                return cat
    return "unknown"


if __name__ == "__main__":
    if len(argv) != 3:
        print(__doc__)
    else:
        # Read data
        df = pd.read_csv(
            argv[1], parse_dates=[[0, 1]], dtype={"zip_code": pd.UInt16Dtype()}
        )
        # set index
        df.set_index("collision_id", inplace=True)

        # fix some column names
        df.rename(
            columns={
                "crash_date_crash_time": "crash_datetime",
                "vehicle_type_code1": "vehicle_type_code_1",
                "vehicle_type_code2": "vehicle_type_code_2",
            },
            inplace=True,
        )

        # Remove unnecessary columns
        df.drop(["location"], axis=1, inplace=True)

        # clean up vehicle types
        df.loc[:, "vehicle_type_code_1":"vehicle_type_code_5"] = df.loc[
            :, "vehicle_type_code_1":"vehicle_type_code_5"
        ].applymap(filter_vehicle)
        # change this to a count of the types
        for cat in ["two-wheel", "normal", "large", "unknown"]:
            df[f"number_of_{cat}_veh"] = (
                df.loc[:, "vehicle_type_code_1":"vehicle_type_code_5"] == cat
            ).sum(axis=1)
        # drop vehicle type cols
        df.drop([f"vehicle_type_code_{i}" for i in range(1, 6)], axis=1, inplace=True)
        # add total vehicle count
        df["total_number_of_vehicles"] = df.loc[
            :, "number_of_two-wheel_veh":"number_of_unknown_veh"
        ].agg(sum, axis=1)

        # Combine all contributing factors in one column
        df["contributing_factors"] = df.loc[
            :, "contributing_factor_vehicle_1":"contributing_factor_vehicle_5"
        ].apply(lambda x: pd.unique(x.dropna()), axis=1)
        # drop vehicle-specific contr factors
        df.drop(
            [f"contributing_factor_vehicle_{i}" for i in range(1, 6)],
            inplace=True,
            axis=1,
        )

        # clean up address strings
        df.loc[:, "on_street_name":"cross_street_name"] = df.loc[
            :, "on_street_name":"cross_street_name"
        ].applymap(lambda s: s.strip() if pd.notna(s) else s)

        # write output file
        df.to_csv(argv[2])
