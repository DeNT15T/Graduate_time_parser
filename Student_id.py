class NumberCalculator:
    def __init__(self, school):
        self.school = school

    def get_number(self, number):
        if self.school is 0:
            return self._NCTU(number)
        elif self.school is 1:
            return self._NCU(number)
        elif self.school is 2:
            return self._NTHU(number)
        elif self.school is 3:
            return self._NYMU(number)


    @staticmethod
    def _NCTU(number):
        number = number[0:2]
        if (number[0] == "0"):
            number = "1" + number
        return number

    @staticmethod
    def _NCU(number):
        if (number[0] == "1"):
            number = number[0:3]
        else:
            number = number[0:2]
        return number


    @staticmethod
    def _NTHU(number):
        if (number[0] == "1"):
            number = number[0:3]
        else:
            number = number[0:2]
        return number


    @staticmethod
    def _NYMU(number):
        number = number[1:3]
        if (number[0] == "0"):
            number = "1" + number
        return number
