from __future__ import unicode_literals

import luigi

from datetime import datetime

from luigi.contrib.spark import PySparkTask
from pyspark.sql.types import StructType
from pyspark.sql import SQLContext, Row
from pyspark.rdd import PipelinedRDD, RDD

from .configurable import Configurable


def validate_in_schema(row, schema):
    # TODO: This is a pretty expensive operation to perform on every write for every row...
    errors = []

    schema_fields = set([field.name for field in schema.fields])
    if isinstance(row, Row):
        row = row.asDict()
    row_fields = row.keys()
    additional_fields = list(row_fields - schema_fields)
    if len(additional_fields) > 0:
        errors.append({
            'error': 'additional fields in the row: %s' % (additional_fields, ),
            'row': row
        })
    # missing_fields = list(schema_fields - row_fields)
    # if len(missing_fields) > 0:
    #     errors.append({
    #         'error': 'missing fields in the row: %s' % (missing_fields, ),
    #         'row': row
    #     })

    for field in schema.fields:
        if isinstance(field.dataType, StructType) and field.name in row:
            errors += validate_in_schema(row[field.name], field.dataType)
        if not field.nullable and row.get(field.name) is None:
            errors.append({
                'error': '%s is not nullable but has a null value or is missing' % (field.name, ),
                'row': row
            })
    return errors


class SparkTask(PySparkTask, Configurable):
    dataset = luigi.Parameter()
    timestamp = luigi.Parameter(default=None)
    frequency = luigi.Parameter(default='microsecond')

    REQUIRED = ['config', 'secrets']

    OPTIONAL = {
        'depends_on': [],
        'store': None,
        'error_handler': None,
        'log_adapter': None
    }

    # TODO: this should be dynamically set when writing to the store
    default_partitions = 4

    spark_packages = []

    OUTPUT = None

    def __init__(self, *args, **kwargs):
        super(SparkTask, self).__init__(*args, **kwargs)
        if self.timestamp is None:
            self.timestamp = datetime.now()
        self.error_handler = None
        self.log_adapter = None
        self._log = None

    def __getstate__(self):
        state = self.__dict__.copy()
        if 'sql_context' in state:
            del state['sql_context']
        if 'sc' in state:
            del state['sc']
        if '_log' in state:
            del state['_log']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def process(self, inputs):
        raise NotImplementedError()

    def complete(self):
        if self.store:
            self.store.frequency = self.frequency,
            self.store.timestamp = self.timestamp
        return super(SparkTask, self).complete()

    def setup(self, conf):
        conf.set('spark.sql.shuffle.partitions', self.default_partitions)

    def requires(self):
        for task in self.depends_on:
            yield task

    def run(self, *args, **kwargs):
        try:
            return super(SparkTask, self).run(*args, **kwargs)
        except Exception as e:
            if self.error_handler:
                self.error_handler.capture(e)
            raise

    def main(self, spark_context, *args):
        self.sc = spark_context
        self.sql_context = SQLContext(spark_context)

        if self.log_adapter:
            self._log = self.log_adapter.logger()

        if self.store:
            self.store.configure(sql_context=self.sql_context)

        output = self.process(self.input())
        schema = self._build_schema()
        if isinstance(output, (PipelinedRDD, RDD)):
            output = self._df_from_rdd(output, schema)
        if hasattr(output, '__iter__'):
            output = self._df_from_iter(output, schema)
        # TODO: detect if type is rdd then _df_from_rdd with schema
        if self.store:
            self.output().write(output)

    def log(self, message):
        if self._log:
            self._log.info(message)

    def _df_from_iter(self, rows, schema):
        rdd = self.sql_context._sc.parallelize(rows)
        return self._df_from_rdd(rdd, schema)

    def _df_from_rdd(self, rdd, schema):
        # TODO: move this schema check to a higher-level, should happen no matter the conversion from list or RDD
        errors = rdd.flatMap(lambda r: validate_in_schema(r, schema)).cache()
        if errors.count() > 0:
            raise ValueError('Schema validation errors in the content', errors.take(10))
        df = self.sql_context.createDataFrame(rdd, schema=schema)
        return df

    def _build_schema(self):
        schema = self.config.get('schema', self.OUTPUT)
        if schema is None:
            return None
        schema = dict(schema)

        def add_defaults(fields):
            new_fields = []
            for field in fields:
                field['metadata'] = field.get('metadata', {})
                field['nullable'] = field.get('nullable', False)
                if 'fields' in field['type']:
                    field['type']['fields'] = add_defaults(field['type']['fields'])
                    field['type']['type'] = 'struct'
                if 'elementType' in field['type']:
                    if 'fields' in field['type']['elementType']:
                        field['type']['elementType']['fields'] = add_defaults(field['type']['elementType']['fields'])
                        field['type']['elementType']['type'] = 'struct'
                    field['type']['containsNull'] = field['type'].get('containsNull', False)
                new_fields.append(field)
            return new_fields
        schema['fields'] = add_defaults(schema['fields'])
        schema['type'] = 'struct'
        return StructType.fromJson(schema)

    def output(self):
        return self.store

    def input(self):
        inputs = super(SparkTask, self).input()
        inputs = {target.dataset: target for target in inputs}
        for task in self.depends_on:
            target = inputs[task.dataset]
            target.configure(
                sql_context=self.sql_context,
                frequency=task.frequency,
                timestamp=task.timestamp
            )
        inputs = {dataset: target.read() for dataset, target in inputs.items()}
        return inputs

    @property
    def name(self):
        return self.dataset

    @property
    def packages(self):
        return list(set(self.store.spark_packages + self.spark_packages))

    def to_df(self, rows):
        return self.sql_context\
                   ._sc\
                   .parallelize(rows)\
                   .map(lambda l: Row(**dict(l)))\
                   .toDF()
