import os
import sys

cwd = os.getcwd()


def main():
    # Make sure there is actually a configuration file
    config_file_dir = os.path.join(cwd, "config.py")
    if not os.path.exists(config_file_dir):
        sys.exit(
            "There dosen't seem to be a configuration file. Have you run the init command?")
    else:
        sys.path.insert(0, cwd)
        try:
            from config import facebook_title, facebook_image, facebook_url, facebook_description
        except:
            sys.exit(
                "We could not find the Facebook card variables in your config.py!")

    card_meta = ""
    card_meta = card_meta + "<meta property=\"og:title\" content=\"" + \
        facebook_title + "\" />\n"
    card_meta = card_meta + "<meta property=\"og:type\" content=\"website\" />\n"
    card_meta = card_meta + "<meta property=\"og:image\" content=\"" + \
        facebook_image + "\" />\n"
    card_meta = card_meta + "<meta property=\"og:url\" content=\"" + \
        facebook_url + "\" />\n"
    card_meta = card_meta + "<meta property=\"og:description\" content=\"" + \
        facebook_description + "\" />\n"

    return card_meta
