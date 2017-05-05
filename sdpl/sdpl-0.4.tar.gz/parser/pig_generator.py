__author__ = 'Bohdan Mushkevych'

from io import TextIOWrapper
from antlr4 import *

import schema.io
from grammar.sdplListener import sdplListener
from grammar.sdplParser import sdplParser
from parser.relation import Relation
from parser.data_store import DataStore
from parser.projection import RelationProjection, ComputableField
from parser.decorator import print_comments
from parser import pig_schema, postresql_schema


class PigGenerator(sdplListener):
    def __init__(self, token_stream: CommonTokenStream, output_stream: TextIOWrapper):
        super().__init__()
        self.token_stream = token_stream
        self.output_stream = output_stream

        # format: {name: Relation}
        self.relations = dict()

    def _out(self, text):
        self.output_stream.write(text)
        self.output_stream.write('\n')

    def _out_bypass_parser(self, ctx: ParserRuleContext):
        """ prints user input *as-is*: retaining all formatting, spaces, special symbols, etc """
        start_index = ctx.start.tokenIndex
        stop_index = ctx.stop.tokenIndex
        user_text = self.token_stream.getText(interval=(start_index, stop_index))
        self._out(user_text)

    @print_comments('--')
    def exitLibDecl(self, ctx: sdplParser.LibDeclContext):
        # REGISTER quotedString (AS ID )? ;
        # 0        1             2  3
        path_child = ctx.getChild(1)      # library path: QuotedStringContext

        if ctx.getChildCount() > 3:
            # read out the AS ID part
            library_alias = ctx.getChild(3)
            self._out('REGISTER {0} AS {1};'.format(path_child.getText(), library_alias.getText()))
        else:
            self._out('REGISTER {0};'.format(path_child.getText()))

    @print_comments('--')
    def exitRelationDecl(self, ctx: sdplParser.RelationDeclContext):
        relation_name = ctx.getChild(0).getText()
        if ctx.getChild(3).getText() == 'TABLE':
            # ID = LOAD TABLE ... FROM ... WITH SCHEMA ... VERSION ... ;
            # 0  1 2    3     4   5    6   7    8      9   10      11
            table_name = ctx.getChild(4).getText()
            repo_path = ctx.getChild(6).getText()
            schema_path = ctx.getChild(9).getText()
            version = ctx.getChild(11).getText()
            relation = Relation(relation_name, schema_path, version)
            self.relations[relation_name] = relation

            # NOTICE: all LOAD specifics are handled by `DataSource` instance
            data_source = DataStore(table_name, repo_path, relation)
            parse_module = pig_schema if data_source.data_repository.is_file_type else postresql_schema
            self._out("{0} = {1};".format(relation_name, parse_module.parse_datasource(data_source)))
        elif ctx.getChild(3).getText() == 'SCHEMA':
            # ID = LOAD SCHEMA ... VERSION ... ;
            # 0  1 2    3      4   5       6
            schema_path = ctx.getChild(4).getText()
            version = ctx.getChild(6).getText()
            self.relations[relation_name] = Relation(relation_name, schema_path, version)
        else:
            ctx_children = [ctx.getChild(i).getText() for i in range(4)]
            clause = ' '.join(ctx_children)
            raise UserWarning('Unknown clause {0}. Expecting either LOAD SCHEMA ... or LOAD TABLE ...'
                              .format(clause))

    @print_comments('--')
    def exitProjectionDecl(self, ctx: sdplParser.ProjectionDeclContext):
        # ID = PROJECTION ( projectionFields ) NOEMIT? ;
        # 0  1 2          3 4                5 7?      8?
        # projectionFields    : projectionField (',' projectionField)* ;
        # projectionField: computeDecl | schemaField ;
        # schemaFields:  schemaField (, schemaField)* ;
        # schemaField :  (-)? ID . ( ID | *) (AS ID)? ;
        relation_name = ctx.getChild(0).getText()
        ctx_proj_fields = ctx.getTypedRuleContexts(sdplParser.ProjectionFieldsContext)
        ctx_proj_fields = ctx_proj_fields[0]    # only one block of projection fields is expected
        projection = self.parse_schema_projection(relation_name, ctx_proj_fields)

        is_silent = ctx.children[-2].getText() == 'NOEMIT'
        if is_silent:
            # schema is projected implicitly, i.e. without output
            return

        # perform schema output
        # step 1: make sure we don't project from more than one schema
        #         as this makes the FOREACH ... GENERATE loop impossible
        output_fields = projection.fields + projection.computable_fields
        right_relations = set(field.schema_name for field in output_fields if field.schema_name)
        if len(right_relations) > 1:
            raise UserWarning('More than one schema is referenced in PROJECTION: *{0}*'.format(right_relations))

        self.emit_schema_projection(projection, relation_name, right_relations.pop())

    def parse_schema_projection(self, relation_name:str, ctx_proj_fields:sdplParser.ProjectionFieldsContext) -> RelationProjection:
        """ method is the heart of the Schema Projection functionality:
            it reads the input, produces projected `Relation`
            and enlists it into the `self.relations` - list of known relations
        """
        projection = RelationProjection(self.relations)
        list_ctx_fields = ctx_proj_fields.getTypedRuleContexts(sdplParser.ProjectionFieldContext)

        def _fetch_by_type(ctx_type:type):
            _fields = list()
            for ctx_proj_field in list_ctx_fields:
                ctx_field = ctx_proj_field.getTypedRuleContexts(ctx_type)
                if not ctx_field:
                    continue
                _fields.append(ctx_field[0])
            return _fields

        schema_fields = _fetch_by_type(sdplParser.SchemaFieldContext)
        self._parse_schema_fields(projection, schema_fields)
        compute_fields = _fetch_by_type(sdplParser.ComputeDeclContext)
        self._parse_compute_expressions(projection, compute_fields)

        self.relations[relation_name] = projection.finalize_relation(relation_name)
        return projection

    def _parse_schema_fields(self, projection:RelationProjection, schema_fields:list):
        for ctx_schema_field in schema_fields:
            assert isinstance(ctx_schema_field, sdplParser.SchemaFieldContext)
            if ctx_schema_field.getChildCount() <= 4:
                # `B.bbb` or `-B.bbb` format
                schema_field = ctx_schema_field.getText()
                schema_name, field_name = schema_field.split('.')
                as_field_name = field_name
            else:
                # `B.bbb AS ccc` format
                schema_field = ''.join(f.getText() for f in ctx_schema_field.children[:-2])
                schema_name, field_name = schema_field.split('.')
                as_field_name = ctx_schema_field.children[-1].getText()  # last list element carries new field name

            do_subtract = schema_field.startswith('-')
            schema_name = schema_name.lstrip('-')

            if field_name == '*':
                if do_subtract:
                    # `-B.*` format
                    projection.remove_all(schema_name)
                else:
                    # `B.*` format
                    projection.add_all(schema_name)
            else:
                if do_subtract:
                    projection.remove(schema_name, field_name)
                else:
                    projection.add(schema_name, field_name, as_field_name)

    def _parse_compute_expressions(self, projection:RelationProjection, compute_fields:list):
        # computeExpression AS typedField ;
        # 0                 1  2
        # typedField      : ID:ID ;
        for ctx_compute_decl in compute_fields:
            assert isinstance(ctx_compute_decl, sdplParser.ComputeDeclContext)
            ctx_compute_expression = ctx_compute_decl.getTypedRuleContexts(sdplParser.ComputeExpressionContext)
            ctx_compute_expression = ctx_compute_expression[0]    # only one block of compute expressions is expected

            typed_field = ctx_compute_decl.children[-1]
            field_name = typed_field.children[0].getText()
            field_type = typed_field.children[-1].getText()

            # read full computing expression string
            start_index = ctx_compute_expression.start.tokenIndex
            stop_index = ctx_compute_expression.stop.tokenIndex
            expression = self.token_stream.getText(interval=(start_index, stop_index))

            comp_field = ComputableField(field_name, field_type, expression)
            projection.new_field(comp_field)

    def emit_schema_projection(self, projection:RelationProjection, left_relation_name, right_relation_name):
        """ method iterates over the projection and emits FOREACH ... GENERATE code
            NOTICE: computable fields are placed at the tail of the GENERATE block """
        output_fields = projection.fields + projection.computable_fields
        self._out('{0} = FOREACH {1} GENERATE'.format(left_relation_name, right_relation_name))
        output = ',\n    '.join([str(f) for f in output_fields])
        self._out('    ' + output)
        self._out(';')

    @print_comments('--')
    def exitExpandSchema(self, ctx:sdplParser.ExpandSchemaContext):
        # EXPAND SCHEMA ID ;
        # 0      1      2
        relation_name = ctx.getChild(2).getText()
        referenced_schema = self.relations[relation_name].schema
        self._out('-- autocode: expanding relation {0} schema'.format(relation_name))
        self._out(pig_schema.parse_schema(referenced_schema))

    @print_comments('--')
    def exitStoreDecl(self, ctx: sdplParser.StoreDeclContext):
        # STORE ID INTO TABLE quotedString FROM quotedString ;
        # 0     1  2    3     4            5    6
        relation_name = ctx.getChild(1).getText()
        table_name = ctx.getChild(4).getText()
        repo_path = ctx.getChild(6).getText()
        relation = self.relations[relation_name]
        data_sink = DataStore(table_name, repo_path, relation)
        parse_module = pig_schema if data_sink.data_repository.is_file_type else postresql_schema
        self._out(parse_module.parse_datasink(data_sink))

    @print_comments('--')
    def exitStoreSchemaDecl(self, ctx: sdplParser.StoreSchemaDeclContext):
        # STORE SCHEMA ID INTO quotedString;
        # 0     1      2  3    4
        relation_name = ctx.getChild(2).getText()
        schema_path = ctx.getChild(4).getText()
        referenced_schema = self.relations[relation_name].schema
        schema.io.store(referenced_schema, schema_path)

    @print_comments('--')
    def exitJoinDecl(self, ctx: sdplParser.JoinDeclContext):
        # ID = JOIN joinElement (, joinElement)+ WITH PROJECTION ( projectionFields );
        # 0  1 2    3            4+
        # joinElement     :  ID 'BY' (relationColumn | relationColumns) ;
        # relationColumns :  '(' relationColumn (',' relationColumn)* ')' ;
        # relationColumn  :  ID ('.' ID) ;

        # step 1: Generate JOIN as JOIN_SA_SB_..._SZ
        relation_name = ctx.getChild(0).getText()
        ctx_join_elements = ctx.getTypedRuleContexts(sdplParser.JoinElementContext)

        join_name = 'JOIN'
        join_body = ''
        for ctx_join_element in ctx_join_elements:
            assert isinstance(ctx_join_element, sdplParser.JoinElementContext)
            element_id = ctx_join_element.getChild(0).getText()
            join_name += '_' + element_id.upper()

            if not join_body:
                # this is the first cycle of the loop
                join_body = 'JOIN {0} BY '.format(element_id)
            else:
                join_body += ', {0} BY '.format(element_id)

            ctx_columns = ctx_join_element.getTypedRuleContexts(sdplParser.RelationColumnsContext)
            ctx_columns = ctx_columns[0]  # only one block of relation columns is expected
            join_body += ctx_columns.getText()

        self._out('{0} = {1} ;'.format(join_name, join_body))

        # step 2: perform schema projection
        ctx_proj_fields = ctx.getTypedRuleContexts(sdplParser.ProjectionFieldsContext)
        ctx_proj_fields = ctx_proj_fields[0]    # only one block of projection fields is expected
        projection = self.parse_schema_projection(relation_name, ctx_proj_fields)

        # step 3: expand schema with FOREACH ... GENERATE
        self.emit_schema_projection(projection, relation_name, join_name)

    @print_comments('--')
    def exitFilterDecl(self, ctx: sdplParser.FilterDeclContext):
        # ID = FILTER ID BY filterExpression ;
        # 0  1 2      3  4  5
        relation_name = ctx.getChild(0).getText()
        source_relation_name = ctx.getChild(3).getText()
        self.relations[relation_name] = self.relations[source_relation_name]
        self._out_bypass_parser(ctx)

    @print_comments('--')
    def exitOrderByDecl(self, ctx: sdplParser.OrderByDeclContext):
        # ID = ORDER ID BY relationColumn (, relationColumn)* ;
        # 0  1 2     3  4  5               6+
        relation_name = ctx.getChild(0).getText()
        source_relation_name = ctx.getChild(3).getText()
        self.relations[relation_name] = self.relations[source_relation_name]
        self._out_bypass_parser(ctx)

    @print_comments('--')
    def exitGroupByDecl(self, ctx: sdplParser.GroupByDeclContext):
        # ID = GROUP ID BY relationColumn (, relationColumn)* ;
        # 0  1 2     3  4  5               6+
        relation_name = ctx.getChild(0).getText()
        source_relation_name = ctx.getChild(3).getText()
        self.relations[relation_name] = self.relations[source_relation_name]
        self._out_bypass_parser(ctx)

    @print_comments('--')
    def exitQuotedCode(self, ctx:sdplParser.QuotedCodeContext):
        # QUOTE_DELIM .*? QUOTE_DELIM ;
        ctx.start = ctx.children[1].symbol  # skipping starting QUOTE_DELIM
        ctx.stop = ctx.children[-2].symbol  # skipping closing QUOTE_DELIM
        self._out('-- quoted source code: start')
        self._out_bypass_parser(ctx)
        self._out('-- quoted source code: finish')
