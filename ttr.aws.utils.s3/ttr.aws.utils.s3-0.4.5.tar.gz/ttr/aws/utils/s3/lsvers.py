import boto3
import argparse
import sys
import datetime
import itertools
import calendar
import plac
import os
import json
from csv import DictWriter
from ConfigParser import SafeConfigParser
from .utils import check_from_to

from pkg_resources import resource_string
templ = resource_string(__name__, 'chart.html')


def load_alias(bucket_key):
    config = SafeConfigParser()
    rcfname = ".s3lsversrc"
    flocs = [os.curdir, os.path.expanduser("~"), "/etc/s3lsvers"]
    config.read([os.path.join(loc, rcfname) for loc in flocs])
    return config.get("aliases", bucket_key)


def get_json_record(dtime, size, age):
    tt = datetime.datetime.timetuple(dtime)
    epoch = calendar.timegm(tt) * 1000
    return [epoch, size, age]


def parse_bucket_key(bucket_key):
    if ("/" not in bucket_key):
        bucket_key = load_alias(bucket_key)
    assert "/" in bucket_key, "bucket_key must be in form 'bucket/key_name'"
    return bucket_key.split("/", 1)


def get_csvwriter(list_file):
    fields = ["key_name", "version_id", "size", "last_modified", "age"]
    if list_file:
        return DictWriter(list_file, fields,
                          delimiter=";", extrasaction="ignore")
    else:
        return None


@plac.annotations(
    profile_name=("AWSCLI profile name", "option"),
    aws_access_key_id=("AWS Access Key ID", "option"),
    aws_secret_access_key=("AWS Secret Access Key", "option"),
    from_time=("start of version modification time range", "option", "from"),
    to_time=("end of version modification time range", "option", "to"),
    list_file=("Name of output CSV file.", "option", None,
               argparse.FileType("wb")),
    html_file=("Name of HTML output file.", "option", None,
               argparse.FileType("wb")),
    version_id=("version-id to start with", "option"),
    bucket_key=("bucket_name/key_name for the key to list", "positional"))
def main(
        bucket_key,
        from_time=None,
        to_time=None,
        list_file=None,
        html_file=None,
        version_id=None,
        profile_name=None,
        aws_access_key_id=None,
        aws_secret_access_key=None):
    """Lists versions of given key, creating CSV or HTML file.
    CSV file can be used e.g. by `s3getvers` command.
    HTML file allows showing feed size and update period in chart.

    Version can be limited by time range `from` - `to`.
    `version-id` allow starting from specific version (back to the past).
    Note, that the listing starts with one version after given `version-id`,
    so the version with `version-id` is NOT INCLUDED.

    Key name is specified as bucket_name/key_name.
    Alternatively it can be an alias defined in .s3lsvers file.

    Times are expressed in RFC 3339 format using Zulu (UTC) timezone.
    Times can be truncated on right side.
    Truncated `from` uses smallest variant with given prefix.
    Truncated `to` uses highest variant with given prefix.

    Missing `from`: use time of the oldest version.
    Missing `to`: use time of the latest version.

    Listing has records with structure:
      `{key_name};{version_id};{size};{last_modified};{age}`
        - key_name
            name of the key (excluding bucket name).

        - version_id
            unique identifier for given version on given bucket.

        - size
            size of key object in bytes

        - last_modified
            RFC 3339 formated time of object modification,
            e.g. `2011-06-22T03:05:09.000Z`

        - age
            difference between last_modified of given version
            and preceding version. It is sort of current
            update interval for that version.
            Expressed in seconds.

        Examples:

        Lists all versions of given `keyname` on `bucket`::

            $ s3lsvers bucketname/keyname

        Lists all versions younger then given time (from given time till now)::

            $ s3lsvers -from 2011-07-19T12:00:00 bucketname/keyname

        Lists all versions older then given time
        (from very first version till given date)::

            $ s3lsvers -to 2011-07-19T12:00:00 bucketname/keyname

        Lists all versions in period betwen `from` and `to` time::

            $ s3lsvers -from 2010-01-01 -to 2011-07-19T12:00:00 \
            bucketname/keyname

        Lists all versions and writes them into csv file named `versions.csv`::

            $ s3lsvers -list-file versions.csv bucketname/keyname

        Lists all versions and write them into html chart file
        named `chart.html`::

            $ s3lsvers -html-file chart.html bucketname/keyname

        Print to stdout, write to csv file and create html chart for all
        versions in given time period.::

            $ s3lsvers -from 2010-01-01 -to 2011-07-19T12:00:00 \
            -list-file versions.csv -html-file chart.html bucketname/keyname

        Using bucket/key_name aliases in .s3lsvers file

        Instead of using long bucket and key names on command line, you may
        define aliases.

        Aliases are specified in file .s3lsvers, which may be located in
        currect directory, home directory or /etc/s3lsvers"

        `.s3lsvers` may look like::

            #.s3lsversrc - definition of some preconfigured bucket/key values
            [DEFAULT]
            pl-base: pl-base.dp.tamtamresearch.com
            cz-base: cz-base.dp.tamtamresearch.com
            sk-base: sk-base.dp.tamtamresearch.com

            #values left to ":" must not contain "/" to prevent
            # confusion with real bucket names
            [aliases]
            plcsr: %(pl-base)s/region/pl/ConsumerServiceReady.xml
            pldfs: %(pl-base)s/region/pl/DataFusionService.xml
            czcsr: %(cz-base)s/region/cz/ConsumerServiceReady.xml
            czdfs: %(cz-base)s/region/cz/DataFusionService.xml
            skcsr: %(sk-base)s/region/sk/ConsumerServiceReady.xml
            skdfs: %(sk-base)s/region/sk/DataFusionService.xml
            skes: %(sk-base)s/region/sk/EventService.xml
            sksr: %(sk-base)s/region/sk/SummaryReports.xml

        The format follows SafeConfigParser rules, see
        http://docs.python.org/2/library/configparser.html#safeconfigparser-objects
    """
    cmdname = os.path.basename(sys.argv[0])

    bucket_name, key_name = parse_bucket_key(bucket_key)

    from_time, to_time = check_from_to(from_time, to_time)

    session = boto3.session.Session(profile_name=profile_name,
                                    aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key)
    s3 = session.resource("s3")
    bucket = s3.Bucket(bucket_name)

    # ver_filter = {"KeyMarker": key_name, "Prefix": key_name}
    ver_filter = {"Prefix": key_name}
    if version_id:
        ver_filter["VersionIdMarker"] = version_id

    versions = bucket.object_versions.filter(**ver_filter)

    try:
        json_data = []
        csvwriter = get_csvwriter(list_file)

        for ver in vergen(versions, key_name, from_time, to_time, working, 600):
            print "Date: {last_modified} Size: {size} Age: {age}".format(**ver)
            if csvwriter:
                csvwriter.writerow(ver)
            if html_file:
                json_data.append(get_json_record(ver[
                                 "atime"], ver["size"], ver["age"]))

        if html_file:
            title = "{bucket_name}:{key_name}".format(**locals())
            json_data = json.dumps(json_data, separators=(",", ":"))
            res = render_html(json_data, title=title)
            html_file.write(res)
    except KeyboardInterrupt:
        print "...cancelled."
    finally:
        if list_file and (not list_file.closed):
            list_file.close()
        if html_file and (not html_file.closed):
            html_file.close()
    return


def working(ver):
    print "version num: {i}, modified: {last_modified}".format(**ver)


def vergen(versions, key_name, from_time, to_time,
           callback=None, callback_after=600):
    """return data
    atime, ka.size. age
    ka.name, ka.version_id, ka.size, ka.last_modified, age

    """
    vers_a, vers_b = itertools.tee(versions)
    vers_b.next()

    def buildver():
        """create dict, describing one version of key"""
        fmt = "{:%Y-%m-%dT%H:%M:%S}.000Z"
        return {"i": i, "atime": atime, "btime": btime, "age": age,
                "key_name": ka.key, "size": ka.size,
                "last_modified": fmt.format(ka.last_modified),
                "version_id": ka.version_id
                }
    for i, ka, kb in itertools.izip(itertools.count(), vers_a, vers_b):
        # if there are keys with the same prefix, we must stop
        # as soon as key_name does not match exactly
        if ka.key != key_name:
            break
        atime = ka.last_modified
        # if there are keys with the same prefix, we report age for last
        # key as 0
        last_modified = atime
        if kb.key == key_name:
            btime = kb.last_modified
            age = (atime - btime).seconds
        else:
            btime = None
            age = 0
        if from_time and (last_modified < from_time):
            break
        elif to_time and (last_modified > to_time):
            if i % callback_after == 0:
                callback(buildver())
            continue
        yield buildver()


def render_html(
        json_data,
        title,
        subtitle="(gzipped) feed size [bytes] and update intervals[seconds]",
        set_1_name="Feed size",
        set_2_name="Update iterval",
        ):
    return templ.format(**locals())


def placer():
    try:
        plac.call(main)
    except Exception as e:
        print e
        raise

if __name__ == "__main__":
    placer()
