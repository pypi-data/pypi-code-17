#!/usr/bin/env python
# preprocess/preprocess_pcmis.py

INCOMPLETE_DO_NOT_USE

"""
===============================================================================
    Copyright (C) 2015-2017 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.
===============================================================================

===============================================================================
PCMIS table structure
===============================================================================
- No proper documentation, but the structure is clear.
- See pcmis_information_schema.ods


- PatientDetails

    PatientID -- PK; patient-defining field; VARCHAR(100)
    FirstName
    LastName
    NHSNumber
    ...

- Other per-patient things: Patient*

- CasesAll

    CaseNumber -- appears to be unique; same #records as ReferralDetails

- Many other per-case things: Case*

    CaseNumber -- FK to CasesAll/ReferralDetails
    
- Group things: linked to cases via GroupMember

- Carers: from PatientCarerDetails (CarerNumber, PatientID)
- Children: from PatientChildDetails (ChildNumber, PatientID)

- ReferralDetails

    CaseNumber -- appears to be unique; same #records as CasesAll
    PatientID -- not unique
    PrimaryDiagnosis (e.g. 'F41.1')

- Non-patient stuff we'll filter out:

    pcmis_UserProfiles
    Users

"""


import argparse
import logging
from typing import Any, List, Optional

from sqlalchemy import (
    create_engine,
    MetaData,
)
from sqlalchemy.engine import Engine
from sqlalchemy.schema import Column, Table
from sqlalchemy.sql.sqltypes import BigInteger, Integer

from crate_anon.anonymise.constants import CHARSET
from crate_anon.common.debugfunc import pdb_run
from crate_anon.common.logsupport import configure_logger_for_colour
from crate_anon.common.sql import (
    add_columns,
    add_indexes,
    assert_view_has_same_num_rows,
    create_view,
    drop_columns,
    drop_indexes,
    drop_view,
    ensure_columns_present,
    execute,
    get_column_names,
    get_table_names,
    get_view_names,
    set_print_not_execute,
    sql_fragment_cast_to_int,
    ViewMaker,
)
from crate_anon.common.sqla import (
    get_single_int_pk_colname,
    get_single_int_autoincrement_colname,
    hack_in_mssql_xml_type,
    make_bigint_autoincrement_column,
)
from crate_anon.preprocess.rio_ddgen import (
    DDHint,
    get_rio_dd_settings,
)

log = logging.getLogger(__name__)


# =============================================================================
# Constants
# =============================================================================

CRATE_COL_PK = "crate_pk"
CRATE_COL_PCMIS_NUMBER = "crate_pcmis_number"
CRATE_COL_NHS_NUMBER = "crate_nhs_number_int"
MASTER_PATIENT_TABLE = "PatientDetails"
PCMIS_COL_PATIENT_ID_COL = "PatientId"


# =============================================================================
# Generic table processors
# =============================================================================

def is_per_case_table(table: Table) -> bool:
    pass


# =============================================================================
# Specific table processors
# =============================================================================


# =============================================================================
# PCMIS views
# =============================================================================



# =============================================================================
# Geography views
# =============================================================================

def add_postcode_geography_view(engine: Engine,
                                progargs: Any,
                                ddhint: DDHint) -> None:  # ddhint modified
    # Re-read column names, as we may have inserted some recently by hand that
    # may not be in the initial metadata.
    if progargs.rio:
        addresstable = RIO_TABLE_ADDRESS
        rio_postcodecol = RIO_COL_POSTCODE
    else:
        addresstable = RCEP_TABLE_ADDRESS
        rio_postcodecol = RCEP_COL_POSTCODE
    orig_column_names = get_column_names(engine, tablename=addresstable,
                                         sort=True)

    # Remove any original column names being overridden by new ones.
    # (Could also do this the other way around!)
    geogcols_lowercase = [x.lower() for x in progargs.geogcols]
    orig_column_names = [x for x in orig_column_names
                         if x.lower() not in geogcols_lowercase]

    orig_column_specs = [
        "{t}.{c}".format(t=addresstable, c=col)
        for col in orig_column_names
    ]
    geog_col_specs = [
        "{db}.{t}.{c}".format(db=progargs.postcodedb,
                              t=ONSPD_TABLE_POSTCODE,
                              c=col)
        for col in sorted(progargs.geogcols, key=lambda x: x.lower())
    ]
    overlap = set(orig_column_names) & set(progargs.geogcols)
    if overlap:
        raise ValueError(
            "Columns overlap: address table contains columns {}; "
            "geogcols = {}; overlap = {}".format(
                orig_column_names, progargs.geogcols, overlap))
    ensure_columns_present(engine, tablename=addresstable, column_names=[
        rio_postcodecol])
    select_sql = """
        SELECT {origcols},
            {geogcols}
        FROM {addresstable}
        LEFT JOIN {pdb}.{pcdtab}
        ON {addresstable}.{rio_postcodecol} = {pdb}.{pcdtab}.pcds
        -- RCEP, and presumably RiO, appear to use the ONS pcds format, of
        -- 2-4 char outward code; space; 3-char inward code.
        -- If this fails, use this slower version:
        -- ON REPLACE({addresstable}.{rio_postcodecol},
        --            ' ',
        --            '') = {pdb}.{pcdtab}.pcd_nospace
    """.format(
        addresstable=addresstable,
        origcols=",\n            ".join(orig_column_specs),
        geogcols=",\n            ".join(geog_col_specs),
        pdb=progargs.postcodedb,
        pcdtab=ONSPD_TABLE_POSTCODE,
        rio_postcodecol=rio_postcodecol,
    )
    create_view(engine, VIEW_ADDRESS_WITH_GEOGRAPHY, select_sql)
    assert_view_has_same_num_rows(engine, addresstable,
                                  VIEW_ADDRESS_WITH_GEOGRAPHY)
    ddhint.suppress_table(addresstable)


# =============================================================================
# Table action selector
# =============================================================================

def process_table(table: Table, engine: Engine, progargs: Any) -> None:
    tablename = table.name
    column_names = table.columns.keys()
    log.debug("TABLE: {}; COLUMNS: {}".format(tablename, column_names))
    if progargs.rio:
        patient_table_indicator_column = get_rio_patient_id_col(table)
    else:  # RCEP:
        patient_table_indicator_column = RCEP_COL_PATIENT_ID

    is_patient_table = (patient_table_indicator_column in column_names or
                        tablename == progargs.full_prognotes_table)
    # ... special for RCEP/CPFT, where a RiO table (with different patient ID
    # column) lives within an RCEP database.
    if progargs.drop_danger_drop:
        # ---------------------------------------------------------------------
        # DROP STUFF! Opposite order to creation (below)
        # ---------------------------------------------------------------------
        # Specific
        if tablename == progargs.master_patient_table:
            drop_for_master_patient_table(table, engine)
        elif tablename == progargs.full_prognotes_table:
            drop_for_progress_notes(table, engine)
        elif progargs.rio and tablename == RIO_TABLE_CLINICAL_DOCUMENTS:
            drop_for_clindocs_table(table, engine)
        # Generic
        if is_patient_table:
            drop_for_patient_table(table, engine)
        else:
            drop_for_nonpatient_table(table, engine)
    else:
        # ---------------------------------------------------------------------
        # CREATE STUFF!
        # ---------------------------------------------------------------------
        # Generic
        if is_patient_table:
            process_patient_table(table, engine, progargs)
        else:
            process_nonpatient_table(table, engine, progargs)
        # Specific
        if tablename == progargs.master_patient_table:
            process_master_patient_table(table, engine, progargs)
        elif progargs.rio and tablename == RIO_TABLE_CLINICAL_DOCUMENTS:
            process_clindocs_table(table, engine, progargs)
        elif tablename == progargs.full_prognotes_table:
            process_progress_notes(table, engine, progargs)


def process_all_tables(engine: Engine,
                       metadata: MetaData,
                       progargs: Any) -> None:
    for table in sorted(metadata.tables.values(),
                        key=lambda t: t.name.lower()):
        process_table(table, engine, progargs)


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Alters a PCMIS database to be suitable for CRATE.")
    parser.add_argument("--url", required=True, help="SQLAlchemy database URL")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")
    parser.add_argument(
        "--print", action="store_true",
        help="Print SQL but do not execute it. (You can redirect the printed "
             "output to create an SQL script.")
    parser.add_argument("--echo", action="store_true", help="Echo SQL")

    parser.add_argument(
        "--drop-danger-drop", action="store_true",
        help="REMOVES new columns and indexes, rather than creating them. "
             "(There's not very much danger; no real information is lost, but "
             "it might take a while to recalculate it.)")

    parser.add_argument(
        "--debug-skiptables", action="store_true",
        help="DEBUG-ONLY OPTION. Skip tables (view creation only)")

    parser.add_argument(
        "--postcodedb",
        help='Specify database (schema) name for ONS Postcode Database (as '
             'imported by CRATE) to link to addresses as a view. With SQL '
             'Server, you will have to specify the schema as well as the '
             'database; e.g. "--postcodedb ONS_PD.dbo"')
    parser.add_argument(
        "--geogcols", nargs="*", default=DEFAULT_GEOG_COLS,
        help="List of geographical information columns to link in from ONS "
             "Postcode Database. BEWARE that you do not specify anything too "
             "identifying. Default: {}".format(' '.join(DEFAULT_GEOG_COLS)))

    parser.add_argument(
        "--settings-filename",
        help="Specify filename to write draft ddgen_* settings to, for use in "
             "a CRATE anonymiser configuration file.")

    progargs = parser.parse_args()

    rootlogger = logging.getLogger()
    configure_logger_for_colour(
        rootlogger, level=logging.DEBUG if progargs.verbose else logging.INFO)

    log.info("CRATE in-place preprocessor for PCMIS databases")
    safeargs = {k: v for k, v in vars(progargs).items() if k != 'url'}
    log.debug("args (except url): {}".format(repr(safeargs)))

    if progargs.postcodedb and not progargs.geogcols:
        raise ValueError(
            "If you specify postcodedb, you must specify some geogcols")

    set_print_not_execute(progargs.print)

    hack_in_mssql_xml_type()

    engine = create_engine(progargs.url, echo=progargs.echo,
                           encoding=CHARSET)
    metadata = MetaData()
    metadata.bind = engine
    log.info("Database: {}".format(repr(engine.url)))  # ... repr hides p/w
    log.debug("Dialect: {}".format(engine.dialect.name))

    log.info("Reflecting (inspecting) database...")
    metadata.reflect(engine)
    log.info("... inspection complete")

    ddhint = DDHint()

    if progargs.drop_danger_drop:
        # Drop views (and view-induced table indexes) first
        drop_pcmis_views(engine, metadata, progargs, ddhint)
        drop_view(engine, VIEW_ADDRESS_WITH_GEOGRAPHY)
        if not progargs.debug_skiptables:
            process_all_tables(engine, metadata, progargs)
    else:
        # Tables first, then views
        if not progargs.debug_skiptables:
            process_all_tables(engine, metadata, progargs)
        if progargs.postcodedb:
            add_postcode_geography_view(engine, progargs, ddhint)
        create_pcmis_views(engine, metadata, progargs, ddhint)

    if progargs.settings_filename:
        with open(progargs.settings_filename, 'w') as f:
            print(get_rio_dd_settings(ddhint), file=f)


if __name__ == '__main__':
    pdb_run(main)
