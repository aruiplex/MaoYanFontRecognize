import MaoYanFontRecognize
import bs4

m = MaoYanFontRecognize.MaoYanFont()
html = open("./movie_test.html", "r")
soup = bs4.BeautifulSoup(html, "html.parser")
spans = soup("span", class_="stonefont")

rate_raw = spans[0].contents[0]
money_unit = soup("span", class_="unit")[0].contents[0] if soup(
    "span", class_="unit") else 1
rate_num_raw = spans[1].contents[0]
money_raw = spans[2].contents[0]
import io
fd = open("./font_test.woff", "rb")
font_file = io.BytesIO(fd.read())

print(m.translate(rate_raw, rate_num_raw, font_file, money_raw, money_unit))