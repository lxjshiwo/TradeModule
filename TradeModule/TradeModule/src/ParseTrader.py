#encoding: utf-8
'''
Created on 2018年7月25日

@author: Administrator
'''
import Constant
import Trader
import Filter
from Filter import HengXingStockInfo



def login_dongbei_trader(user_name,user_password):
    pass
#     print(user_name,user_password)

def login_guojun_trader(user_name,user_password):
    pass
#     print(user_name,user_password)

def login_hengtai_trader(user_name,user_password,user_id):
    print(user_name,user_password,user_id)
    tmp_trader = Trader(Constant.HENGXIN_IP,
                        Constant.TRADE_PORT,
                        user_name,
                        user_password,
                        '0',
                        Constant.HENGXIN_YYB,
                        Constant.DLL_PATH,
                        None,
                        sh_code = '',
                        sz_code = '',
                        )
    tmp_trader.query_positions(Constant.QUERY_STOCKS)
    stock_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
    tmp_trader.query_positions(Constant.QUERY_PROPERTY)
    property_input = tmp_trader.trader_Ree.value.decode('gbk','ignore').split('|')
    hengxin_stock_info = HengXingStockInfo(stock_input,property_input,user_name)
    hengxin_stock_info.update_stock_info()
    

def parse_trader_type(x,login_info):
    switcher = {
        '1':login_dongbei_trader,
        '2':login_guojun_trader,
        '3':login_hengtai_trader,
        '4':login_hengtai_trader,
    }
    func = switcher.get(x,'1')
    return func(login_info['userName'],login_info['password'],login_info['userId'])
    
