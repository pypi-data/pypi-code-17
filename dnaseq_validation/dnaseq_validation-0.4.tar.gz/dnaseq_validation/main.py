#!/usr/bin/env python

import argparse
import json
import logging
import os
import sqlite3
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='log.txt',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S_%Z',
    )
    logger = logging.getLogger(__name__)
    return logger


def run_tests(input_sqlite_metrics):
    test_dict = dict()
    conn = sqlite3.connect(input_sqlite_metrics)
    c = conn.cursor()

    sql_count_fastq_files = c.execute('select count(distinct(fastq)) from fastqc_data_Basic_Statistics')
    sql_count_fastq_files_result = sql_count_fastq_files.fetchall()[0][0]
    test_dict['count_fastq_files'] = int(sql_count_fastq_files_result)

    sql_count_files_output = c.execute('select count(distinct(filename)) from integrity')
    sql_count_files_output_result = sql_count_files_output.fetchall()[0][0]
    test_dict['count_files_output'] = int(sql_count_files_output_result)

    sql_count_readgroups = c.execute('select count(distinct(ID)) from readgroups')
    sql_count_readgroups_result = sql_count_readgroups.fetchall()[0][0]
    test_dict['count_readgroups'] = int(sql_count_readgroups_result)

    sql_bases_mapped_samtools_stats = c.execute('select "bases mapped" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_bases_mapped_samtools_stats_result = sql_bases_mapped_samtools_stats.fetchall()[0][0]
    test_dict['bases_mapped_samtools_stats'] = int(sql_bases_mapped_samtools_stats_result)

    sql_average_quality_samtools_stats = c.execute('select "average quality" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_average_quality_samtools_stats_result = sql_average_quality_samtools_stats.fetchall()[0][0]
    test_dict['average_quality_samtools_stats'] = float(sql_average_quality_samtools_stats_result)

    sql_bases_duplicated_samtools_stats = c.execute('select "bases duplicated" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_bases_duplicated_samtools_stats_result = sql_bases_duplicated_samtools_stats.fetchall()[0][0]
    test_dict['bases_duplicated_samtools_stats'] = int(sql_bases_duplicated_samtools_stats_result)

    sql_pairs_diff_chr_samtools_stats = c.execute('select "pairs on different chromosomes" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_pairs_diff_chr_samtools_stats_result = sql_pairs_diff_chr_samtools_stats.fetchall()[0][0]
    test_dict['pairs_diff_chr_samtools_stats'] = int(sql_pairs_diff_chr_samtools_stats_result)

    sql_pairs_other_orient_samtools_stats = c.execute('select "pairs with other orientation" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_pairs_other_orient_samtools_stats_result = sql_pairs_other_orient_samtools_stats.fetchall()[0][0]
    test_dict['pairs_other_orient_samtools_stats'] = int(sql_pairs_other_orient_samtools_stats_result)

    sql_raw_total_seq_samtools_stats = c.execute('select "raw total sequences" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_raw_total_seq_samtools_stats_result =sql_raw_total_seq_samtools_stats.fetchall()[0][0]
    test_dict['raw_total_seq_samtools_stats'] = int(sql_raw_total_seq_samtools_stats_result)

    sql_reads_mq0_samtools_stats = c.execute('select "reads MQ0" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_reads_mq0_samtools_stats_result = sql_reads_mq0_samtools_stats.fetchall()[0][0]
    test_dict['reads_mq0_samtools_stats'] = int(sql_reads_mq0_samtools_stats_result)

    sql_reads_dup_samtools_stats = c.execute('select "reads duplicated" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_reads_dup_samtools_stats_result = sql_reads_dup_samtools_stats.fetchall()[0][0]
    test_dict['reads_dup_samtools_stats'] = int(sql_reads_dup_samtools_stats_result)

    sql_reads_mapped_samtools_stats = c.execute('select "reads mapped" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_reads_mapped_samtools_stats_result = sql_reads_mapped_samtools_stats.fetchall()[0][0]
    test_dict['reads_mapped_samtools_stats'] = int(sql_reads_mapped_samtools_stats_result)

    sql_reads_mapped_and_paired_samtools_stats = c.execute('select "reads mapped and paired" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_reads_mapped_and_paired_samtools_stats_result = sql_reads_mapped_and_paired_samtools_stats.fetchall()[0][0]
    test_dict['reads_mapped_and_paired_samtools_stats'] = int(sql_reads_mapped_and_paired_samtools_stats_result)

    sql_reads_paired_samtool_stats = c.execute('select "reads paired" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_reads_paired_samtool_stats_result = sql_reads_paired_samtool_stats.fetchall()[0][0]
    test_dict['reads_paired_samtool_stats'] = int(sql_reads_paired_samtool_stats_result)

    sql_reads_prop_paired_samtools_stats = c.execute('select "reads properly paired" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_reads_prop_paired_samtools_stats_result = sql_reads_prop_paired_samtools_stats.fetchall()[0][0]
    test_dict['reads_prop_paired_samtools_stats'] = int(sql_reads_prop_paired_samtools_stats_result)

    sql_read_unmapped_samtools_stats = c.execute('select "reads unmapped" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_read_unmapped_samtools_stats_result = sql_read_unmapped_samtools_stats.fetchall()[0][0]
    test_dict['read_unmapped_samtools_stats'] = int(sql_read_unmapped_samtools_stats_result)

    sql_seqs_samtools_stats = c.execute('select "sequences" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_seqs_samtools_stats_result = sql_seqs_samtools_stats.fetchall()[0][0]
    test_dict['seqs_samtools_stats'] = int(sql_seqs_samtools_stats_result)

    sql_total_length_samtools_stats = c.execute('select "total length" from samtools_stats where input_state = "markduplicates_readgroups"')
    sql_total_length_samtools_stats_result =sql_total_length_samtools_stats.fetchall()[0][0]
    test_dict['total_length_samtools_stats'] = int(sql_total_length_samtools_stats_result)

    sql_read_pairs_picard_markduplicates = c.execute('select READ_PAIRS_EXAMINED from picard_MarkDuplicates where input_state = "markduplicates_readgroups"')
    sql_read_pairs_picard_markduplicates_result = sql_read_pairs_picard_markduplicates.fetchall()[0][0]
    test_dict['read_pairs_picard_markduplicates'] = int(sql_read_pairs_picard_markduplicates_result)

    sql_read_pair_dups_picard_markduplicates = c.execute('select READ_PAIR_DUPLICATES from picard_MarkDuplicates where input_state = "markduplicates_readgroups"')
    sql_read_pair_dups_picard_markduplicates_result = sql_read_pair_dups_picard_markduplicates.fetchall()[0][0]
    test_dict['read_pair_dups_picard_markduplicates'] = int(sql_read_pair_dups_picard_markduplicates_result)

    conn.close()
    return test_dict


def get_expected(input_json_expected_metrics):
    json_file = open(input_json_expected_metrics)
    json_str = json_file.read()
    json_data = json.loads(json_str)
    return json_data


def write_results(results):
    with open('results.json', 'w') as outfile:
        json.dump(results, outfile, sort_keys=True, indent=4, ensure_ascii=True)
    return


def compare_test_expected(input_sqlite_metrics, input_json_expected_metrics, logger):
    test_dict = run_tests(input_sqlite_metrics)
    expected_dict = get_expected(input_json_expected_metrics)

    if sorted(test_dict.keys()) != sorted(expected_dict.keys()):
        logging.debug('sorted(test_dict.keys()):\n%s' % sorted(test_dict.keys()))
        logging.debug('sorted(expected_dict.keys()):\n%s' % sorted(expected_dict.keys()))
        logger.debug('test_dict keys do not match expected_dict keys')
        sys.exit(1)

    test_results = dict()
    for test_key in sorted(test_dict.keys()):
        test_value = test_dict[test_key]
        expected_value = expected_dict[test_key]
        test_result = (test_value == expected_value)
        phrase = 'matches' if test_result else 'DOES NOT MATCH'
        logger.info(test_key + ': expected value ' + str(expected_value) + ' ' + phrase + ' test value ' + str(test_value))
        test_results[test_key] = test_result

    final_result_value = True
    for test_key in sorted(test_results.keys()):
        final_result_value = (final_result_value and test_results[test_key])

    results = {'overall' : final_result_value, 'steps' : test_results}
    write_results(results)


def main():
    parser = argparse.ArgumentParser('GDC DNASeq Validation')
    parser.add_argument('--input_sqlite_metrics',
                        required=True
    )
    parser.add_argument('--input_json_expected_metrics',
                        required=False
    )
    args = parser.parse_args()
    input_sqlite_metrics = args.input_sqlite_metrics
    input_json_expected_metrics = args.input_json_expected_metrics

    logger = setup_logging()

    compare_test_expected(input_sqlite_metrics, input_json_expected_metrics, logger)
    return


if __name__ == '__main__':
    main()
