import argparse
import sys

import bs4
import requests

from reportlab.pdfgen import canvas


def parse_args():
    descr = "Generate PDFs from Slideshare presentations"

    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('url', metavar='url', nargs=1,
                        help='the URL to slurp')
    parser.add_argument('--output', '-o', default='out.pdf',
                        help='the file to write to (default: out.pdf)')

    return parser.parse_args()


def main():
    args = parse_args()

    res = requests.get(args.url[0])

    tree = bs4.BeautifulSoup(res.text, "html.parser")
    c = canvas.Canvas(args.output)

    for img in tree.findAll("img", class_="slide_image"):
        img_url = img.attrs["data-full"]
        page_width, page_height = c._pagesize
        c.setPageRotation(90)
        c.drawImage(img_url, 0, 0, page_height, page_width, preserveAspectRatio=True)
        c.showPage()
    c.save()


if __name__ == '__main__':
    main()
