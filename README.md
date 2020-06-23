# slurm-stats
extract slurm job stats

It uses slurm's sacct to extract job stats.
It stores the last timestamp in a file called "lasttimestamp".
This means the tool can fetch all jobs since the last time stamp.
If there is no stored timestime it defaults to fetching all jobs since midnight.

## Install

Requires python3:

    yum install python3-pip python3-devel libyaml-devel
    pip3 install ClusterShell

To run the script, try this cron ready example:

    TZ=UTC python3 sacct.py >>jobstats.txt
