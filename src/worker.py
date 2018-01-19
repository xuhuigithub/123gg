#!/usr/bin/env python
# encoding: utf-8
"""
@ref: https://github.com/Jack-Cherish/python-spider/blob/master/12306.py
"""
from splinter.browser import Browser
from time import sleep
import logging
from splinter.exceptions import ElementDoesNotExist
import threading

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s [%(threadName)s]")
logger = logging.getLogger(__name__)


"""
map
1 -> 硬座
2 -> 软座
3 -> 硬卧

"""


class huoche(object):
    # 用户名，密码
    username = u"xxxx"
    passwd = u"xxxx"

    starts = u"%u5317%u4EAC%2CBJP"  # 北京
    ends = u"%u5FB7%u5DDE%2CDZP"  # 德州

    # 时间格式2018-01-19
    dtime = u"2018-02-14"
    ###乘客名
    users = [u"徐晖", u"徐松", u"徐月", u"黄俊英"]

    """网址"""
    ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
    login_url = "https://kyfw.12306.cn/otn/login/init"
    initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
    buy = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

    def __init__(self):
        self.driver_name = 'chrome'
        self.executable_path = 'D:/chromedriver'

    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill("loginUserDTO.user_name", self.username)
        # sleep(1)
        self.driver.fill("userDTO.password", self.passwd)
        logger.info(u"等待验证码，自行输入...")
        while True:
            if self.driver.url != self.initmy_url:
                sleep(1)
            else:
                break


    def start(self):
        self.driver = Browser(driver_name=self.driver_name)
        self.login()

        self.driver.visit(self.ticket_url)
        try:
            print(u"购票页面开始...")
            # sleep(1)
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})

            self.driver.reload()        #add cookies 后的reload 重新让页面读cookies
            self.driver.find_by_text(u"查询").click()

            while self.driver.url == self.ticket_url:
                try:
                    ticket_tr = self.driver.find_by_id(
                        'ticket_{ver_train_number}'.format(ver_train_number='240000K1010B'))
                    ticket_tr.find_by_css('.btn72').first.click()
                except ElementDoesNotExist:
                    self.driver.find_by_text(u"查询").click()         #如果没有就再刷新一次
                    logger.info("继续查！")
                    sleep(5)
                else:
                    sleep(5)  # 为了避免龟速网
            logger.info(u"开始预订...")
            sleep(1)
            logger.info(u'开始选择用户和选座...')
            for u_i, user in enumerate(self.users):
                u_i += 1
                self.driver.find_by_text(user).last.click()
                user_tr = self.driver.find_by_id('seatType_%s' % u_i).first
                try:
                    user_tr.find_by_xpath('//option[contains(text(), "{seat}")]'.format(seat=u"硬座")).first.click()
                except ElementDoesNotExist:
                    user_tr.find_by_xpath('//option[contains(text(), "{seat}")]'.format(seat=u"无座")).first.click()
            logger.info(u"提交订单...")
            self.driver.find_by_id('submitOrder_id').click()
            sleep(1.5)
            logger.info(u"最后确认...")
            # self.driver.find_by_id('qr_submit_id').click()        #最后提交，打开升天

        except Exception as e:
            raise e


if __name__ == '__main__':
    huoche = huoche()
    T = threading.Thread(target=huoche.start)
    T.start()
    # huoche.start()
