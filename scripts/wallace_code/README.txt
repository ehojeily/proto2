CONTENTS

bad_rows_removed_5min : Proto2 data with improper metadata removed (data here is part of an intermediate step and should not be used for analysis!)
csv : Fully time-corrected proto2 data (this should be what's used for analysis)

-----------------------------------------------------------------------------------------------------------------------------------------------------

This folder contains corrected csvs of raw Proto2 data found in 
/data/aq/inhouse/raw/aqmon002

Corrections are applied using the dec_proto2_timelag_correction.ipynb file in this directory

Corrections were applied by comparing 5 minute interval proto2 pressure readings against NYSM data at the same time interval.
Periods with large variance in the difference between these two readings are flagged and visually inspected for any signs of lag in the data. If lag was detected, this data was shifted by 5 minute increments until the lag was eliminated.   

This data is stored within the /csv subdirectory in this folder.


Data stored within the /bad_rows_removed_5min subdirectory is raw proto2 data that's been resampled to 5 minute intervals and partially quality controlled.

Within the original raw proto2 data, there is a tendency for some days to populate data columns with column header information. This crashes any program trying to read the data. Data within this folder should always be used for analysis over the raw data!

This was performed using the proto2_remove_bad_rows.ipynb file within this subdirectory.
