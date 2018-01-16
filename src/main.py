#!/usr/bin/env python
# encoding: utf-8
'''
查询两站之间的火车票信息

输入参数： <date> <from> <to>

12306 api:
'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2017-07-18&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=SZH&purpose_codes=ADULT'

'''
HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "https://kyfw.12306.cn/otn/leftTicket/init",
    'Cache-Control': 'no-store'
}
import requests
import time
import logging
from stations import stations_dict
from sms import sms_send

# logger
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s [%(threadName)s]")
logger = logging.getLogger(__name__)

# 关闭https证书验证警告
requests.packages.urllib3.disable_warnings()

# 城市名代码查询字典
# key：城市名 value：城市代码


# 反转k，v形成新的字典
code_dict = {v: k for k, v in stations_dict.items()}


def get_query_url(text):
    '''
    返回调用api的url链接
    '''
    # 解析参数
    args = str(text).split(' ')
    try:
        date = args[0]
        from_station_name = args[1]
        to_station_name = args[2]
        from_station = stations_dict[from_station_name]
        to_station = stations_dict[to_station_name]
    except:
        date, from_station, to_station = '--', '--', '--'
        # 将城市名转换为城市代码

    # api url 构造
    url = (
        'https://kyfw.12306.cn/otn/leftTicket/queryZ?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT'
    ).format(date, from_station, to_station)
    logger.info(url)
    return url


def query_train_info(url):
    '''
    查询火车票信息：
    返回 信息查询列表
    '''
    result = dict()
    result['info_list'] = []
    try:
        r = requests.get(url,headers=HEADERS,verify=False)
        # 获取返回的json数据里的data字段的result结果
        raw_trains = r.json()['data']['result']

        for raw_train in raw_trains:
            # 循环遍历每辆列车的信息
            data_list = raw_train.split('|')

            # 车次号码
            train_no = data_list[3]
            # 出发站
            from_station_code = data_list[6]
            from_station_name = code_dict[from_station_code]
            # 终点站
            to_station_code = data_list[7]
            to_station_name = code_dict[to_station_code]
            # 出发时间
            start_time = data_list[8]
            # 到达时间
            arrive_time = data_list[9]
            # 总耗时
            time_fucked_up = data_list[10]
            # 一等座
            first_class_seat = data_list[31] or '无'
            # 二等座
            second_class_seat = data_list[30] or '无'
            # 软卧
            soft_sleep = data_list[23] or '无'
            # 硬卧
            hard_sleep = data_list[28] or '无'
            # 硬座
            hard_seat = data_list[29] or '无'
            # 无座
            no_seat = data_list[26] or '无'

            if no_seat != "无" or hard_seat != "无" and "VNP" not in data_list:   #过滤掉动车，高铁
                info = ('车次:{train_no},出发时间:{start_time},到达时间:{arrive_time}'.format(train_no=train_no,
                                                                                    start_time=start_time,
                                                                                    arrive_time=arrive_time
                                                                                    ))
                result['info_list'].append(info)
    except Exception as e:
        print(r.text)
        logger.warning(str(e))
    finally:
        return result


if __name__ == '__main__':
    while True:
        info_list = query_train_info(get_query_url(u"2018-02-14 北京 德州")).get('info_list')
        if info_list:
            logger.info(sms_send(receiver=17710399068, msg=str(info_list), timeout=5))
            # logger.info(sms_send(receiver=17710399068, msg=str(info_list), timeout=5))
            time.sleep(60)
        else:
            time.sleep(5)