class codes_style:
    def __init__(self, color: bool = False, reverse: bool = False, codes: bool = True):
        """
        生成一个codes_style类

        :param color: 是否是24位彩色 反之使用黑白
        :param reverse: 是否字符反转
        :param codes: 是否使用字符 反之使用色块
        """
        self.color = color
        self.reverse = reverse
        self.codes = codes
