#!/usr/bin/env python

import argparse
import datetime
import logging
import os
import time

import sqlalchemy
import pandas as pd

def setup_logging(args, uuid):
    logging.basicConfig(
        filename=os.path.join(uuid + '.log'),
        level=args.level,
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S_%Z',
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

def main():
    parser = argparse.ArgumentParser('update status of job')
    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)

    parser.add_argument('--created_bai_gdc_id',
                        required=True
    )
    parser.add_argument('--created_bam_gdc_id',
                        required=True
    )
    parser.add_argument('--created_sqlite_gdc_id',
                        required=True
    )
    parser.add_argument('--hostname',
                        required=True
    )
    parser.add_argument('--host_ipaddress',
                        required=True
    )
    parser.add_argument('--host_macaddress',
                        required=True
    )
    parser.add_argument('--input_bam_gdc_id',
                        required=True
    )
    parser.add_argument('--job_creation_uuid',
                        required=True
    )
    parser.add_argument('--known_snp_gdc_id',
                        required=True
    )
    parser.add_argument('--program_id',
                        required=True
    )
    parser.add_argument('--project_id',
                        required=True
    )
    parser.add_argument('--reference_amb_gdc_id',
                        required=True
    )
    parser.add_argument('--reference_ann_gdc_id',
                        required=True
    )
    parser.add_argument('--reference_bwt_gdc_id',
                        required=True
    )
    parser.add_argument('--reference_fa_gdc_id',
                        required=True
    )
    parser.add_argument('--reference_fai_gdc_id',
                        required=True
    )
    parser.add_argument('--reference_pac_gdc_id',
                        required=True
    )
    parser.add_argument('--reference_sa_gdc_id',
                        required=True
    )
    parser.add_argument('--run_uuid',
                        required=True
    )
    parser.add_argument('--runner_cwl_path',
                        required=True
    )
    parser.add_argument('--runner_cwl_branch',
                        required=True
    )
    parser.add_argument('--runner_cwl_repo',
                        required=True
    )
    parser.add_argument('--runner_cwl_repo_hash',
                        required=True
    )
    parser.add_argument('--runner_job_path',
                        required=True
    )
    parser.add_argument('--runner_job_branch',
                        required=True
    )
    parser.add_argument('--runner_job_repo',
                        required=True
    )
    parser.add_argument('--runner_job_repo_hash',
                        required=True
    )
    parser.add_argument('--slurm_resource_cores',
                        required=True,
                        type=int
    )
    parser.add_argument('--slurm_resource_disk_gb',
                        required=True,
                        type=int
    )
    parser.add_argument('--slurm_resource_mem_mb',
                        required=True,
                        type=int
    )
    parser.add_argument('--status',
                        required=True
    )
    parser.add_argument('--status_table',
                        required=True
    )
    parser.add_argument('--thread_count',
                        required=True,
                        type=int
    )

    args = parser.parse_args()
    run_uuid = args.run_uuid

    logger = setup_logging(args, run_uuid)

    sqlite_name = run_uuid + '.db'
    engine_path = 'sqlite:///' + sqlite_name
    engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')

    time_seconds = time.time()
    datetime_now = str(datetime.datetime.now())
    
    status_dict = dict()
    status_dict['datetime_now'] = datetime_now
    status_dict['time_seconds'] = time_seconds
    status_dict['run_uuid'] = [run_uuid]
    for arg in vars(args):
        if arg != 'run_uuid':
            status_dict[arg] = getattr(args, arg)

    df = pd.DataFrame(status_dict)
    df.to_sql(args.status_table, engine, if_exists='append')
    return

if __name__ == '__main__':
    main()
