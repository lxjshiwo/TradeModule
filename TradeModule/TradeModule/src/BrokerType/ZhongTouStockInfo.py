import logging
import math
import DbControler
from Filter import AbstractStockInfo
import time


class ZhongTouStockInfo(AbstractStockInfo):

    def __init__(self,stock_info_block,property_block,entrust_block,sec_hold_user,finish_book_block,user_id):
        self.user_id = user_id
        self.sec_hold_user = sec_hold_user
        # 资金信息块
        self.property_block = property_block
        # # 交易委托块
        self.entrust_block = entrust_block
        # # 交易完成委托块
        self.finish_book_block = finish_book_block


        self.cur_index_list = ['sec_code',  # '证券代码'
                               'sec_name',  # '证券名称'
                               'sec_amount',  # '股份余额'
                               'sec_stock_amount',  #'可用股份'
                               'sec_cur_rcc',  # '成本价'
                               'sec_cur_price',  # '当前价'
                               'sec_rpl_rcc',  # '当前成本',

                               'sec_cur_lmv',  # '最新市值'
                               'sec_ref_rpl',  # '浮动盈亏',
                               'sec_rpl_ratio',  # '盈亏比例(%)'

                               'sec_trade_amount',  # '冻结数量'
                               'sec_error_amount',  # '异常冻结'
                               'sec_way_amount',  # '在途股份'
                               'sec_now_amount',  # '当前持股'
                               'sec_buy_rcc',  # '买入成本',

                               'sec_buy_average',  # '买入均价',
                               'sec_real_rpl',  # '实际盈亏',



                               'sec_share_code',  # '股东代码'
                               'sec_account_type',  # '帐号类别'
                               'sec_exchange_code',  # '交易所代码'
                               'sec_account',  #'资金帐号
                               'sec_trade_user_code',  # '客户代码'


                               'sec_trade_market',  ## '交易所名称', ',
                               'sec_trade_user_position',  # '交易席位'

                               'sec_ref_info',  # '方案类型'
                               'sec_handler',  #产品标志
                               'sec_reference_information',  # '保留信息'
                               ]

        # 当前相应账户的持仓类别

        self.cur_property_list = [
            #'资金帐号',
            'pro_account',
            # '币种'
            'pro_type',
            # '资金余额'
            'pro_amount',
            # '可用资金'
            'pro_use',
            # '可取资金'
            'pro_avail',
            # '冻结资金'
            'pro_freezed',
            # '总资产'
            'pro_total',
            # '回购金额'
            'pro_inverse_amounts',
            # '最新市值'
            'pro_now',


            # '保留信息'
            'reserve_information',
        ]
        # 当前委托信息
        self.cur_entrust_list = [
            #'委托日期',
            'en_date',
            # '委托时间'
            'en_time',
            # '证券代码'
            'en_code',
            # '证券名称'
            'en_name',
            # '买卖标志'
            'en_side_1',
            # '买卖标志'
            'en_side_2',
            # '委托价格'
            'en_price',
            # '委托数量'
            'en_amount',
            # '委托编号'
            'en_number',
            # '成交数量'
            'en_deal_amount',
            # '成交价格'
            'en_deal_price',
            #成交均价
            'en_deal_ave_price',
            #撤单数量
            'en_cancel_amount',
            #状态说明
            'en_status',
            # 撤单标志
            'en_cancel_label',
            # '股东代码'
            'en_user_code',
            # '帐号类别'
            'en_count_type',
            # '资金帐号',
            'en_account_code',
            # '交易名称'
            'en_trade_market',
            #备注
            'en_ref_info',
            #句柄
            'en_handler',
            # '保留信息'
            'en_ref_data',
        ]
        # 当前用户成交股票信息
        self.cur_trade_list = [
            #'成交日期'
            'tr_date',
            # '成交时间'
            'tr_time',
            # '证券代码'
            'tr_code',
            # '证券名称'
            'tr_name',
            # '买卖标志'
            'tr_side',
            # '买卖标志'
            'tr_flag',
            #'委托价格',
            'tr_en_price',
            # '委托数量'
            'tr_en_amount',
            # '委托编号'
            'tr_en_code',
            # '成交价格'
            'tr_price',
            # '成交数量'
            'tr_amount',
            # '成交金额'
            'tr_cost',
            # '成交编号'
            'tr_suc_code',
            # '股东代码'
            'tr_mrkt_code',
            # '帐号类别'
            'tr_type',
            #状态说明
            'tr_status',
            #'交易所名称',
            'tr_market',
            # '备注'
            'tr_ref_info',
            # '撤单标志'
            'tr_cancel_flag',
            #句柄
            'tr_handler',
            # '保留信息',
            'tr_ref_information',
        ]
        # 当前股票名称
        self.stock_list = []
        # 当前所有股票块
        self.all_stock_info = {}
        # 当前所有持仓信息
        self.property_info = {}
        # 当前委托列表
        self.entrust_list = []
        # 当前委托块
        self.all_entrust_info = {}
        # 当日成交列表
        self.deal_list = []
        # 当日成交列表明细
        self.all_deal_info = {}

        self.stock_info_block = stock_info_block

    def _format_stock(self,**kwargs):
        start = 2
        step = int(self.stock_info_block[0])
        count = math.floor(len(self.stock_info_block) / step )
        for col in range(count):
            tmp_stock = {}
            if col == 0:
                continue
            else:
                start += step
                for row in range(step):
                    if self.stock_info_block[start+row] == '':
                        tmp_stock[self.cur_index_list[row]] = 0
                    else:
                        tmp_stock[self.cur_index_list[row]] = self.stock_info_block[start+row]
                self.stock_list.append(tmp_stock['sec_code'])
                self.all_stock_info[tmp_stock['sec_code']] = tmp_stock
        stock_info_list = []
        for code in self.stock_list:
            out_stock = {}
            out_stock['po_StockCode'] = self.all_stock_info[code]['sec_code']
            out_stock['po_StockName'] = self.all_stock_info[code]['sec_name'].encode('utf-8').decode('utf-8')
            out_stock['po_StockMuch'] = self.all_stock_info[code]['sec_amount']
            out_stock['po_Inventory'] = self.all_stock_info[code]['sec_amount']
            out_stock['po_SellMuch'] = self.all_stock_info[code]['sec_trade_amount']
            out_stock['po_CostMoney'] = self.all_stock_info[code]['sec_cur_rcc']
            out_stock['po_NowMoney'] = self.all_stock_info[code]['sec_cur_price']
            out_stock['po_Market'] = self.all_stock_info[code]['sec_cur_lmv']
            out_stock['po_PL'] = self.all_stock_info[code]['sec_ref_rpl']
            out_stock['po_PLRatio'] = self.all_stock_info[code]['sec_rpl_ratio']
            stock_info_list.append(out_stock)
        DbControler.insert_position_table(stock_info_list, self.user_id)
        print("inserted position table")
        logging.debug("inserted position table")

    # 格式化相应资金持仓情况
    def _format_property(self, **kwargs):
            start = 2
            step = int(self.property_block[0])
            count = int(self.property_block[1]) + 1
            tmp_property = {}
            if count == 1:
                logging.debug("no property")
            else:
                for col in range(count):
                    if col == 0:
                        continue
                    else:
                        start += step
                        for row in range(step):
                            if self.property_block[start + row] == '':
                                tmp_property[self.cur_property_list[row]] = 0
                            else:
                                tmp_property[self.cur_property_list[row]] = self.property_block[start + row]
                        self.property_info = tmp_property
                    property_info_list = []
                    out_property = {}

                    out_property['fu_PL'] = self.property_info['pro_type']

                    out_property['fu_GetMoney'] = self.property_info['pro_avail']

                    out_property['fu_Market'] = self.property_info['pro_now']

                    out_property['fu_AvailableMoney'] = self.property_info['pro_use']
                    out_property['fu_Total'] = self.property_info['pro_total']


                    property_info_list.append(out_property)
                    print(property_info_list)
                    DbControler.insert_fund_table(property_info_list, self.user_id)
                    logging.debug("inserted fund table")
                    print("inserted fund table")

    # 格式化相应的交易明细
    def _format_entrust(self, **kwargs):
        start = 2
        step = int(self.entrust_block[0])
        count = int(self.entrust_block[1]) + 1
        print(self.entrust_block)
        if count == 1:
            print("no entrust")
            logging.debug("no entrust")
        else:
            for col in range(count):
                tmp_entrust = {}
                if col == 0:
                    continue
                else:
                    start += step
                    for row in range(step):
                        #                         print(self.cur_entrust_list[row])
                        if self.entrust_block[start + row] == '':
                            tmp_entrust[self.cur_entrust_list[row]] = 'null'
                        else:
                            tmp_entrust[self.cur_entrust_list[row]] = self.entrust_block[start + row]
                    self.entrust_list.append(tmp_entrust['en_number'])
                    self.all_entrust_info[tmp_entrust['en_number']] = tmp_entrust
            entrust_info_list = []
            for entrust in self.entrust_list:
                out_entrust = {}
                out_entrust['et_Date'] = time.strftime("%Y-%m-%d")
                out_entrust['et_OperateDate'] = time.strftime("%Y-%m-%d")
                raw_time = self.all_entrust_info[entrust]['en_time']
                out_entrust['et_OperateTime'] = raw_time[:2] + ":" + raw_time[2:4] + ":" + raw_time[4:]
                out_entrust['et_StockCode'] = self.all_entrust_info[entrust]['en_code']
                out_entrust['et_StockName'] = self.all_entrust_info[entrust]['en_name']
                out_entrust['et_SignId'] = self.all_entrust_info[entrust]['en_side_1']
                out_entrust['et_Money'] = self.all_entrust_info[entrust]['en_price']
                out_entrust['et_Much'] = self.all_entrust_info[entrust]['en_amount']
                out_entrust['et_Number'] = self.all_entrust_info[entrust]['en_number']
                out_entrust['et_DealMuch'] = '1'
                out_entrust['et_DealMoney'] = '1'
                out_entrust['et_DanMuch'] = '1'
                out_entrust['et_Status'] = '1'
                entrust_info_list.append(out_entrust)
            DbControler.insert_entrust_table(entrust_info_list, self.user_id)
            print("inserted entrust table")
            logging.debug("inserted entrust table")