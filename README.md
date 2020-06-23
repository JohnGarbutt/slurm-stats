# slurm-stats
extract slurm job stats

It uses slurm's sacct to extract job stats of finished jobs.
It stores the last timestamp in a file called "lasttimestamp".
This means the tool can fetch all jobs since the last time stamp.
If there is no stored timestime it defaults to fetching all jobs since midnight.

Note: the default OpenHPC install doesn't enable the accounting service.
It appears this must be enabled before --starttime and --endtime options work as expected.

## Install

Requires python3:

    yum install python3-pip python3-devel libyaml-devel
    pip3 install ClusterShell

To run the script, try this cron ready example:

    rm -f lasttimestamp  # clear any old state, default to today's job
    TZ=UTC python3 sacct.py >>finished_jobs.json

For example, you would expect output a bit like this:

    tail -n2 finished_jobs.json
    {'JobID': '20', 'JobIDRaw': '20', 'Cluster': 'linux', 'Partition': 'normal', 'Account': '', 'Group': 'centos', 'GID': '1000', 'User': 'centos', 'UID': '1000', 'Submit': '2020-06-23T12:43:17', 'Eligible': '2020-06-23T12:43:17', 'Start': '2020-06-23T12:43:21', 'End': '2020-06-23T12:43:23', 'Elapsed': '00:00:02', 'ExitCode': '1:0', 'State': 'FAILED', 'NNodes': '1', 'NCPUS': '1', 'ReqCPUS': '1', 'ReqMem': '500Mc', 'ReqGRES': '', 'ReqTRES': 'bb/datawarp=2800G,billing=1,cpu=1,mem=500M,node=1', 'Timelimit': '5-00:00:00', 'NodeList': 'c1', 'JobName': 'use-perjob.sh', 'AllNodes': ['c1']}
    {'JobID': '21', 'JobIDRaw': '21', 'Cluster': 'linux', 'Partition': 'normal', 'Account': '', 'Group': 'centos', 'GID': '1000', 'User': 'centos', 'UID': '1000', 'Submit': '2020-06-23T12:45:30', 'Eligible': '2020-06-23T12:45:30', 'Start': '2020-06-23T12:45:33', 'End': '2020-06-23T12:45:35', 'Elapsed': '00:00:02', 'ExitCode': '1:0', 'State': 'FAILED', 'NNodes': '1', 'NCPUS': '1', 'ReqCPUS': '1', 'ReqMem': '500Mc', 'ReqGRES': '', 'ReqTRES': 'bb/datawarp=2800G,billing=1,cpu=1,mem=500M,node=1', 'Timelimit': '5-00:00:00', 'NodeList': 'c1', 'JobName': 'use-perjob.sh', 'AllNodes': ['c1']}

# OpenDistro Setup

Best to see the data via Elasticsearch. We used OpenDistro.

Get started here:
https://opendistro.github.io/for-elasticsearch-docs/docs/install/docker/

## Install Filebeat

Be sure to use the oss filebeat, e.g.
https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-7.7.0-x86_64.rpm

Be sure to do add something like this to filebeat config:

    setup.ilm.enabled: false
    xpack.monitoring.enabled: false
    output.elasticsearch:
      hosts: ["localhost:9200"]
      protocol: "https"
      ssl.verification_mode: none
      username: "admin"
      password: "admin"

Then execute the setup:

    sudo filebeat modules enable system
    sudo filebeat setup -e --dashboards --pipelines --template
    sudo systemctl start filebeat

To parse the files as json, add this:

    filebeat.inputs:
    - type: log
      json.add_error_key: true
      paths:
         - '/mnt/ohpc/centos/*.json'
