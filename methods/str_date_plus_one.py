import datetime
def str_date_plus_one(str_dtae):
    '''
    此方法用于字符串形式的日期增加一天，例如输入’2018-06-30‘，则返回’2018-07-01‘；
    :param str_dtae: 2018-06-30
    :return: 2018-07-01
    '''
    try:
        new_date = datetime.datetime.strptime(str_dtae, '%Y-%m-%d') + datetime.timedelta(1)
        new_date_str = datetime.datetime.strftime(new_date, "%Y-%m-%d")
    except:
        print('请输入正确的日期字符串格式：2018-06-07')
        return
    return new_date_str

if __name__ == '__main__':
    print(str_date_plus_one('2021-02-28'))
