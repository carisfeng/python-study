#day02
"""
class 的知识:
两个下划线开头的变量是私有变量，外部无法访问，不推荐使用。

一个下划线开头的变量只是用来标识为私有变量，但是还是可以访问。
"""
from time import sleep


class Clock(object):
    """数字时钟"""

    def __init__(self, hour=0, minute=0, second=0):
        """初始化方法

        :param hour: 时
        :param minute: 分
        :param second: 秒
        """
        self.__hour = hour
        self._minute = minute
        self._second = second

    def run(self):
        """走字"""
        self._second += 1
        if self._second == 60:
            self._second = 0
            self._minute += 1
            if self._minute == 60:
                self._minute = 0
                self.__hour += 1
                if self.__hour == 24:
                    self.__hour = 0

    def show(self):
        """显示时间"""
        return '%02d:%02d:%02d' % \
               (self.__hour, self._minute, self._second)


def main():
    clock = Clock(22, 59, 58)
    while True:
        print(clock.show())
        sleep(1)
        clock.run()
        #print(clock.__hour)
        #AttributeError: 'Clock' object has no attribute '__hour'


if __name__ == '__main__':
    main()