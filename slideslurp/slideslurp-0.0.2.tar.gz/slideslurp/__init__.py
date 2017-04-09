import sys

import bs4
import requests

from reportlab.pdfgen import canvas


def main():
    url = sys.argv[1]

    res = requests.get(url)

    tree = bs4.BeautifulSoup(res.text, "html.parser")
    c = canvas.Canvas('out.pdf')

    for img in tree.findAll("img", class_="slide_image"):
        img_url = img.attrs["data-full"]
        page_width, page_height = c._pagesize
        c.setPageRotation(90)
        c.drawImage(img_url, 0, 0, page_height, page_width, preserveAspectRatio=True)
        c.showPage()
    c.save()


if __name__ == '__main__':
    main()
