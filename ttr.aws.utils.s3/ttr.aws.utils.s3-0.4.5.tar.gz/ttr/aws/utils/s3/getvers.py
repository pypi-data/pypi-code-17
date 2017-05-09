import argparse
import csv
from itertools import izip, count
import botocore
from boto3.session import Session
import plac
from .saver import ObjectVersionSaver, FnameFactory


@plac.annotations(
    profile_name=("""Name of AWSCLI profile to use for credentials""",
                  "option"),
    aws_access_key_id=("Your AWS Access Key ID", "option"),
    aws_secret_access_key=("Your AWS Secret Access Key", "option"),
    bucket_name=("bucket name (default: %(default)s)", "positional"),
    csv_version_file=("name of CSV file with version_id", "positional", None,
                      argparse.FileType("rb")),
    output_version_id_names=("Resulting file names shall use version_id "
                             "to become distinguished "
                             "(default is to use timestamp of file creation)",
                             "flag"),
    no_decompression=("Keeps the files as they come, do not decompress, "
                      "if they come compressed", "flag")
)
def main(bucket_name,
         csv_version_file,
         output_version_id_names=False,
         no_decompression=False,
         profile_name=None,
         aws_access_key_id=None,
         aws_secret_access_key=None):
    """Fetch file versions as listed in provided csv file

    Typical csv file (as by default produced by s3lsvers) is:

        m/y.xml;OrUr6XO8KSKEHbd8mQ.MloGcGlsh7Sir;191;2012-05-23T20:45:10.000Z;39
        m/y.xml;xhkVOy.dJfjSfUwse8tsieqjDicp0owq;192;2012-05-23T20:44:31.000Z;62
        m/y.xml;oKneK.N2wS8pW8.EmLqjldYlgcFwxN3V;193;2012-05-23T20:43:29.000Z;58

    and has columns:
    :key_name: name of the feed (not containing the bucket name itself)
    :version_id: string, identifying unique version. Any following columns can
        contain anything.
    :size: size in bytes. This column is not used and can be missing.
    :last_modified: date, when the version was posted. This column is not used
        and can be missing.

    Typical use (assuming, above csv file is available under name verlist.csv)::

        $ %(prog)s yourbucketname verlist.csv

    What will create following files in current directory:

    * m/f.xml.2012-05-23T20_45_10.xml
    * m/f.xml.2012-05-23T20_44_31.xml
    * m/f.xml.2012-05-23T20_43_29.xml

    Even though these files are gzipped on server, they will be decompressed on
    local disk.
    """
    to_decompress = () if no_decompression else ("deflate", "gzip")

    session = Session(profile_name=profile_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    s3 = session.resource("s3")
    if output_version_id_names:
        fname_factory = FnameFactory().version_id
    else:
        fname_factory = FnameFactory().last_modified
    saver = ObjectVersionSaver(s3, fname_factory, to_decompress)
    try:
        recmsg = "{i:2d}: key_name: {key_name}, version_id: {version_id}"
        for i, row in izip(count(),
                           csv.reader(csv_version_file, delimiter=";")):
            key_name, version_id = row[:2]
            print(recmsg.format(**locals()))
            fname, key = saver.save(bucket_name, key_name, version_id)
            print("resulting file name: {fname}".format(fname=fname))
    except botocore.exceptions.ClientError as e:
        msg = ("Problem accessing bucket object.\n"
               "Possible causes:\n"
               "- missing/wrong credentials\n"
               "- missing bucket or object\n"
               "- no permission to access the object.")
        print(e)
        print(msg)
        return
    except KeyboardInterrupt:
        print("...terminated.")

    return


def placer():
    plac.call(main)

if __name__ == "__main__":
    plac.call(main)
