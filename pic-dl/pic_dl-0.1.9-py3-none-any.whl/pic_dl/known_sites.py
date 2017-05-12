#!/usr/bin/env python3

version = "0.1.9"

SITES = {
        "weibo": "weibo",
        "twitter": "twitter",
        "tumblr": "tumblr",
        "tuchong": "tuchong",
        "lofter": "lofter",
        "bcy": "bcy",
        "163": "163",
        "poco": "poco",
        }

description = "pic-dl: v{}\n\nSupported site: {}"\
                .format(version, "\n\t" + "\n\t".join(list(SITES.keys())))
