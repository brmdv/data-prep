"""Preprocess NYC crashed dataset. An exact walkthrough can be found in the accompanying Notebook file.

Usage:
    python crashes.py INPUTFILE OUTPUTFILE
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
        df.rename(
            columns={"crash_date_crash_time": "crash_datetime"}, inplace=True
        )  # simplify date column name

        # Remove unnecasary columns
        df.drop(["location"], axis=1, inplace=True)
        
        # write output file
        df.to_csv(argv[2])
