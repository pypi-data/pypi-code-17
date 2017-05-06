from __future__ import absolute_import

from bs4 import BeautifulSoup
import requests


html = requests.get("https://en.wikipedia.org/wiki/IOS_SDK").content
soup = BeautifulSoup(html, 'html.parser')
version_tables = soup.select(".wikitable")

# TODO: CLI to update the builds.yml automatically.
# TODO: Add handling for merged cells.


for table in version_tables[2:]:
    build_history = table.find_all("tr")[2:]
    for row in build_history:
        version = None
        build_number = None
        beta = False
        final = False
        try:
            version = row.find("th").text.replace("[edit]", "").replace("\n", "")
            if "final" in version.lower():
                final = True

            if "beta" in version.lower():
                beta = True
        except:
            pass

        try:
            build_number = row.find_all("td")[0].text
        except:
            pass

        if build_number and version:
            print """{build}:
    name: "{version}"
    build: "{build}"
    beta: {beta}
    final: {final}
            
    """.format(version=version, build=build_number, beta=beta, final=final)
