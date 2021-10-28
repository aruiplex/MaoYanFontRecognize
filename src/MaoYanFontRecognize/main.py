import io
import math
import bs4
import os 
from fontTools.ttLib import TTFont
import pkgutil
from importlib import resources

class MaoYanFont():
    """From MaoYan offical web font to translate from chars to numbers.
    """

    def __init__(self):
        # base font to recognize other fonts.
        # The path of package is
        # d = pkgutil.get_data("MaoYanFontRecognize", "data/iconfont0.woff")
        with resources.path("MaoYanFontRecognize", "iconfont0.woff") as path:
            path_str = str(path)
            # print(path_str)
            self.font_base = TTFont(path_str)
            

    def _max_points_in_region(self, l, d) -> float:
        """Count the points number of every points in a certain region.

        Args:
            l (list of tuple): coordinates list of a font 
            d (list of tuple): coordinates list of the other font

        Returns:
            p(float): The accuracy rate of the two list. 
        """
        n = 0
        for dd in d:
            for ll in l:
                # Find the nearest point
                r = math.sqrt((dd[0]-ll[0])**2 + (dd[1]-ll[1])**2)
                if r <= 10:
                    n += 1
                    l.remove(ll)
                    break
        # Accuracy
        p = n / len(d)
        return p

    def _base_number_to_code(self, x):
        return {
            1: "uniE83C",
            2: "uniEA5E",
            3: "uniF6D1",
            4: "uniF882",
            5: "uniE39D",
            6: "uniF139",
            7: "uniF223",
            8: "uniF7A6",
            9: "uniEBF7",
            0: "uniF1C0"
        }[x]

    def _set_new_fonts(self, font_new_path):
        """Setup the another font. 

        Args:
            font_new_path (str): the new font path
        """
        self.font_new = TTFont(font_new_path)

    def _char2num(self, new_code: str) -> int:
        """The main function of class, used to get the index of highest accuracy rate of two coordinate lists, 
            which is the number most likely.  

        Args:
            new_code (str): the unicode of the new font, which need to be identify to a number.

        Returns:
            int: the number which is identified by the recognize
        """
        # change the form of font label
        new_code = "uni" + \
            new_code.encode("unicode_escape").decode()[-4:].upper()
        coordinates_new = list(self.font_new["glyf"][new_code].coordinates)
        one_hot = []
        # try to calculate the accuracy of 10 number, get the index of highest accuracy rate.
        for i in range(0, 10):
            coordinates_base = self.font_base["glyf"][self._base_number_to_code(
                i)].coordinates
            one_hot.append(self._max_points_in_region(
                coordinates_new, coordinates_base))

        return one_hot.index(max(one_hot))

    def _maoyan_formatter(self, chars: bs4.element.NavigableString, money_unit=None):
        units_zh = {"万": 1e4, "亿": 1e8, "万美元": 63900.0}
        result = ""
        base = 1
        # to due with the money unit in the html
        if money_unit != None:
            base *= units_zh[money_unit]

        if chars[-1] in units_zh:
            base *= units_zh[chars[-1]]
            chars = chars[:-1]

        for char in chars:
            if char == ".":
                result += "."
                continue
            i = str(self.char_to_num.char2num(char))
            result += i

        return float(result)*base

    def translate(self, rate_raw: bs4.element.NavigableString, rate_num_raw: bs4.element.NavigableString, font_file: io.BytesIO, money_raw: bs4.element.NavigableString = -1, money_unit=1):
        """tranlate 

        Args:
            rate_raw (str): raw format of rate
            rate_num_raw (str): raw format of rate number 
            font_file (io.BytesIO): BytesIO format of  font file 
            money_raw (int, optional): money of movie, but some movies are null. Defaults to -1.
            money_unit (int, optional): the unit of money. There are three form: "万": 1e4, "亿": 1e8, "万美元": 63900.0. Defaults to 1.
        """
        self._set_new_fonts(font_file)
        rate = self._maoyan_formatter(rate_raw)
        rate_num = self._maoyan_formatter(rate_num_raw)
        if money_raw != -1:
            money = self._maoyan_formatter(money_raw, money_unit)
        return rate, rate_num, money


# m = MaoYanFont()
# m.translate()
