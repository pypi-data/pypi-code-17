'''
The MIT License (MIT)

Copyright (c) 2014-2017 The OmniDB Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import Spartacus.Database, Spartacus.Utils

'''
------------------------------------------------------------------------
Generic
------------------------------------------------------------------------
'''
class Generic(object):
    @staticmethod
    def InstantiateDatabase(p_db_type,
                            p_server,
                            p_port,
                            p_service,
                            p_user,
                            p_password,
                            p_schema,
                            p_conn_id,
                            p_alias):

        if p_db_type == 'postgresql':
            return PostgreSQL(p_server, p_port, p_service, p_user, p_password, p_schema, p_conn_id, p_alias)
        if p_db_type == 'sqlite':
            return SQLite(p_service, p_conn_id, p_alias)

'''
------------------------------------------------------------------------
PostgreSQL
------------------------------------------------------------------------
'''
class PostgreSQL:
    def __init__(self, p_server, p_port, p_service, p_user, p_password, p_schema, p_conn_id, p_alias):
        self.v_alias = p_alias
        self.v_db_type = 'postgresql'
        self.v_conn_id = p_conn_id
        self.v_server = p_server
        self.v_port = p_port
        self.v_service = p_service
        self.v_user = p_user
        self.v_connection = Spartacus.Database.PostgreSQL(p_server, p_port, p_service, p_user, p_password)

        self.v_has_schema = True
        self.v_has_functions = True
        self.v_has_procedures = False
        self.v_has_sequences = True
        self.v_has_primary_keys = True
        self.v_has_foreign_keys = True
        self.v_has_uniques = True
        self.v_has_indexes = True
        self.v_has_update_rule = True

        self.v_default_string = "text"

        self.v_can_rename_table = True
        self.v_rename_table_command = "alter table #p_table_name# rename to #p_new_table_name#"

        self.v_create_pk_command = "constraint #p_constraint_name# primary key (#p_columns#)"
        self.v_create_fk_command = "constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#"
        self.v_create_unique_command = "constraint #p_constraint_name# unique (#p_columns#)"

        self.v_can_alter_type = True
        self.v_alter_type_command = "alter table #p_table_name# alter #p_column_name# type #p_new_data_type#"

        self.v_can_alter_nullable = True
        self.v_set_nullable_command = "alter table #p_table_name# alter #p_column_name# drop not null"
        self.v_drop_nullable_command = "alter table #p_table_name# alter #p_column_name# set not null"

        self.v_can_rename_column = True
        self.v_rename_column_command = "alter table #p_table_name# rename #p_column_name# to #p_new_column_name#"

        self.v_can_add_column = True
        self.v_add_column_command = "alter table #p_table_name# add column #p_column_name# #p_data_type# #p_nullable#"

        self.v_can_drop_column = True
        self.v_drop_column_command = "alter table #p_table_name# drop #p_column_name#"

        self.v_can_add_constraint = True
        self.v_add_pk_command = "alter table #p_table_name# add constraint #p_constraint_name# primary key (#p_columns#)"
        self.v_add_fk_command = "alter table #p_table_name# add constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#"
        self.v_add_unique_command = "alter table #p_table_name# add constraint #p_constraint_name# unique (#p_columns#)"

        self.v_can_drop_constraint = True
        self.v_drop_pk_command = "alter table #p_table_name# drop constraint #p_constraint_name#"
        self.v_drop_fk_command = "alter table #p_table_name# drop constraint #p_constraint_name#"
        self.v_drop_unique_command = "alter table #p_table_name# drop constraint #p_constraint_name#"

        self.v_create_index_command = "create #p_uniqueness# index #p_index_name# on #p_table_name# (#p_columns#)"
        self.v_create_index_command = "create index #p_index_name# on #p_table_name# (#p_columns#)";
        self.v_create_unique_index_command = "create unique index #p_index_name# on #p_table_name# (#p_columns#)"

        self.v_drop_index_command = "drop index #p_schema_name#.#p_index_name#"

        self.v_can_rename_sequence = True
        self.v_can_drop_sequence = True

        self.v_can_alter_sequence_min_value = True
        self.v_can_alter_sequence_max_value = True
        self.v_can_alter_sequence_curr_value = True
        self.v_can_alter_sequence_increment = True

        self.v_create_sequence_command = "create sequence #p_sequence_name# increment #p_increment# minvalue #p_min_value# maxvalue #p_max_value# start #p_curr_value#"
        self.v_alter_sequence_command = "alter sequence #p_sequence_name# increment #p_increment# minvalue #p_min_value# maxvalue #p_max_value# restart #p_curr_value#"
        self.v_rename_sequence_command = "alter sequence #p_sequence_name# rename to #p_new_sequence_name#"
        self.v_drop_sequence_command = "drop sequence #p_sequence_name#"

        self.v_update_rules = [
            "NO ACTION",
			"RESTRICT",
			"SET NULL",
			"SET DEFAULT",
			"CASCADE"
        ]
        self.v_delete_rules = [
            "NO ACTION",
			"RESTRICT",
			"SET NULL",
			"SET DEFAULT",
			"CASCADE"
        ]

        if not p_schema:
            self.v_schema = 'public'
        else:
            self.v_schema = p_schema

    def GetName(self):
        return self.v_service

    def PrintDatabaseInfo(self):
        return self.v_user + "@" + self.v_service + " - " + self.v_schema

    def PrintDatabaseDetails(self):
        return self.v_server + ":" + self.v_port

    def HandleUpdateDeleteRules(self, p_update_rule, p_delete_rule):

        v_rules = ''

        if p_update_rule.strip() != "":
            v_rules += " on update " + p_update_rule + " "
        if p_delete_rule.strip() != "":
            v_rules += " on delete " + p_delete_rule + " "

        return v_rules

    def TestConnection(self):

        v_return = ''

        try:
            self.v_connection.Open()

            v_schema = self.v_connection.Query("select schema_name from information_schema.schemata where lower(schema_name)='" + self.v_schema.lower() + "'")
            if len(v_schema.Rows) > 0:
                v_return = "Connection successful."
            else:
                "Connection successful but schema '" + self.v_schema + "' does not exist."

            self.v_connection.Close()
        except Exception as exc:
            v_return = str(exc)

        return v_return

    def QueryTables(self, p_all_schemas=False):

        v_filter = ''

        if not p_all_schemas:
            v_filter = "  and lower(table_schema) = '{0}' ".format(str.lower(self.v_schema))
        else:
            v_filter = " and lower(table_schema) not in ('information_schema','pg_catalog') "

        return self.v_connection.Query('''
            select lower(table_name) as table_name,
                   lower(table_schema) as table_schema
            from information_schema.tables
            where table_type = 'BASE TABLE'
            {0}
            order by table_schema,table_name
        '''.format(v_filter))

    def QueryTablesFields(self, p_table=None):

        v_filter = ''

        if p_table:
            v_filter = "and lower(c.table_name) = '{0}' ".format(str.lower(p_table))

        return self.v_connection.Query('''
            SELECT lower(c.table_name) as table_name,
                   lower(c.column_name) as column_name,
                   lower(c.data_type) as data_type,
                   c.is_nullable as nullable,
                   c.character_maximum_length as data_length,
                   c.numeric_precision as data_precision,
                   c.numeric_scale as data_scale
            from information_schema.columns c
            join information_schema.tables t on (c.table_name = t.table_name and c.table_schema = t.table_schema)
            where lower(t.table_schema) ='{0}'
              and t.table_type = 'BASE TABLE'
            {1}
            order by c.table_name, c.ordinal_position
        '''.format(str.lower(self.v_schema),v_filter))

    def QueryTablesForeignKeys(self, p_table=None):

        v_filter = ''

        if p_table:
            v_filter = "and lower(KCU1.TABLE_NAME) = '{0}' ".format(str.lower(p_table))

        return self.v_connection.Query('''
            SELECT *
            FROM (SELECT distinct
            lower(KCU1.CONSTRAINT_NAME) AS constraint_name,
            lower(KCU1.TABLE_NAME) AS table_name,
            lower(KCU1.COLUMN_NAME) AS column_name,
            lower(KCU2.CONSTRAINT_NAME) AS r_constraint_name,
            lower(KCU2.TABLE_NAME) AS r_table_name,
            lower(KCU2.COLUMN_NAME) AS r_column_name,
            lower(KCU1.constraint_schema) as table_schema,
            lower(KCU2.constraint_schema) as r_table_schema,
            KCU1.ORDINAL_POSITION,
            RC.update_rule as update_rule,
            RC.delete_rule as delete_rule
            FROM (SELECT *
                  FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS RC
                  WHERE lower(RC.constraint_schema) = '{0}') RC
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU1 ON KCU1.CONSTRAINT_CATALOG = RC.CONSTRAINT_CATALOG
            AND KCU1.CONSTRAINT_SCHEMA = RC.CONSTRAINT_SCHEMA
            AND KCU1.CONSTRAINT_NAME = RC.CONSTRAINT_NAME
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU2
            ON KCU2.CONSTRAINT_CATALOG = RC.UNIQUE_CONSTRAINT_CATALOG
            AND KCU2.CONSTRAINT_SCHEMA = RC.UNIQUE_CONSTRAINT_SCHEMA
            AND KCU2.CONSTRAINT_NAME = RC.UNIQUE_CONSTRAINT_NAME
            AND KCU2.ORDINAL_POSITION = KCU1.ORDINAL_POSITION
            {1}
            ) t
            order by CONSTRAINT_NAME,
            TABLE_NAME,
            ORDINAL_POSITION
        '''.format(str.lower(self.v_schema),v_filter))

    def QueryTablesPrimaryKeys(self, p_schema=None, p_table=None):

        v_filter = ''
        v_curr_schema = ''

        if not p_schema:
            v_curr_schema = self.v_schema
        else:
            v_curr_schema = p_schema

        if p_table:
            v_filter = "and lower(tc.table_name) = '{0}' ".format(str.lower(p_table))

        return self.v_connection.Query('''
            SELECT lower(tc.constraint_name) as constraint_name,
            lower(kc.column_name) as column_name,
            lower(tc.table_name) as table_name
            from
            information_schema.table_constraints tc,
            information_schema.key_column_usage kc
            where
            tc.constraint_type = 'PRIMARY KEY'
            and kc.table_name = tc.table_name
            and kc.table_schema = tc.table_schema
            and kc.constraint_name = tc.constraint_name
            and lower(tc.table_schema)='{0}'
            {1}
            order by tc.constraint_name,
            tc.table_name,
            kc.ordinal_position
        '''.format(str.lower(v_curr_schema),v_filter))

    def QueryTablesUniques(self, p_schema=None, p_table=None):

        v_filter = ''
        v_curr_schema = ''

        if not p_schema:
            v_curr_schema = self.v_schema
        else:
            v_curr_schema = p_schema

        if p_table:
            v_filter = "and lower(tc.table_name) = '{0}' ".format(str.lower(p_table))

        return self.v_connection.Query('''
            SELECT lower(tc.constraint_name) as constraint_name,
            lower(kc.column_name) as column_name,
            lower(tc.table_name) as table_name
            from information_schema.table_constraints tc,
            information_schema.key_column_usage kc
            where tc.constraint_type = 'UNIQUE'
            and kc.table_name = tc.table_name
            and kc.table_schema = tc.table_schema
            and kc.constraint_name = tc.constraint_name
            and lower(tc.table_schema)='{0}'
            {1}
            order by tc.constraint_name,
            tc.table_name,
            kc.ordinal_position
        '''.format(str.lower(v_curr_schema),v_filter))

    def QueryTablesIndexes(self, p_table=None):

        v_filter = ''

        if p_table:
            v_filter = "and lower(t.tablename) = '{0}' ".format(str.lower(p_table))

        return self.v_connection.Query('''
            SELECT lower(t.tablename) as table_name,
            lower(t.indexname) as index_name,
            unnest(string_to_array(replace(substr(t.indexdef, strpos(t.indexdef, '(')+1, strpos(t.indexdef, ')')-strpos(t.indexdef, '(')-1), ' ', ''),',')) as column_name,
            (case when strpos(t.indexdef, 'UNIQUE') > 0 then 'Unique' else 'Non Unique' end) as uniqueness
            from pg_indexes t
            where lower(t.schemaname) = '{0}'
            {1}
            order by t.tablename, t.indexname
        '''.format(str.lower(self.v_schema),v_filter))

    def QueryDataLimited(self, p_query=None, p_count=-1):

        v_filter = ''

        if p_count != -1:
            v_filter = " limit  " + p_count

        return self.v_connection.Query('''
            SELECT *
            from ( {0} ) t
            {1}
        '''.format(p_query,v_filter),True)

    def QueryTableRecords(self, p_column_list, p_table, p_filter, p_count=-1):

        v_limit = ''
        if p_count != -1:
            v_limit = ' limit ' + p_count

        return self.v_connection.Query('''
            select {0}
            from {1} t
            {2}
            {3}
        '''.format(
                p_column_list,
                p_table,
                p_filter,
                v_limit
            )
        )

    def QueryFunctions(self):

        return self.v_connection.Query('''
            select n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' as id,
                   p.proname as name
            from pg_proc p,
                 pg_namespace n
            where p.pronamespace = n.oid
              and lower(n.nspname) = '{0}'
            order by 1
        '''.format(self.v_schema.lower()))

    def QueryFunctionFields(self, p_function):

        return self.v_connection.Query('''
            select y.type::character varying as type,
                   y.name
            from (
                select 'O' as type,
                       'return ' || format_type(p.prorettype, null) as name
                from pg_proc p,
                     pg_namespace n
                where p.pronamespace = n.oid
                  and n.nspname = '{0}'
                  and n.nspname || '.' || p.proname || '(' || oidvectortypes(p.proargtypes) || ')' = '{1}'
            ) y
            union all
            select x.type::character varying as type,
                   trim(x.name) as name
            from (
                select 'I' as type,
                unnest(regexp_split_to_array(pg_get_function_identity_arguments('{1}'::regprocedure), ',')) as name
            ) x
            where length(trim(x.name)) > 0
            order by 1 desc, 2 asc
        '''.format(self.v_schema.lower(), p_function))

    def GetFunctionDefinition(self, p_function):

        v_tmp = '-- DROP FUNCTION {0};\n\n'.format(p_function)
        return v_tmp + self.v_connection.ExecuteScalar("select pg_get_functiondef('{0}'::regprocedure)".format(p_function))

    def QueryProcedures(self):
        return None

    def QueryProcedureFields(self, p_procedure):
        return None

    def QueryProcedureDefinition(self, p_procedure):
        return None

    def QuerySequences(self, p_sequence=None):

        v_filter = ''
        if p_sequence:
            v_filter = "and lower(sequence_name) = '{0}'".format(p_sequence.lower())

        v_table = self.v_connection.Query('''
            select lower(sequence_name) as sequence_name,
                   minimum_value,
                   maximum_value,
                   0 as current_value,
                   increment
            from information_schema.sequences
            where lower(sequence_schema) = '{0}' {1}
        '''.format(self.v_schema.lower(), v_filter))

        for i in range(0, len(v_table.Rows)):
            v_table.Rows[i]['current_value'] = self.v_connection.ExecuteScalar(
                "select last_value from {0}.{1}".format(self.v_schema, v_table.Rows[i]['sequence_name'])
            )

        return v_table

'''
------------------------------------------------------------------------
SQLite
------------------------------------------------------------------------
'''
class SQLite:
    def __init__(self, p_service, p_conn_id, p_alias):
        self.v_alias = p_alias
        self.v_db_type = 'sqlite'
        self.v_conn_id = p_conn_id
        self.v_service = p_service
        self.v_connection = Spartacus.Database.SQLite(p_service)

        self.v_has_schema = False
        self.v_has_functions = False
        self.v_has_procedures = False
        self.v_has_sequences = False
        self.v_has_primary_keys = True
        self.v_has_foreign_keys = True
        self.v_has_uniques = True
        self.v_has_indexes = True
        self.v_schema = ''

    def GetName(self):
        return self.v_service

    def PrintDatabaseInfo(self):
        return self.v_service

    def PrintDatabaseDetails(self):
        return 'Local File'
