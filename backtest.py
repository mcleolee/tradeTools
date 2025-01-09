# 这是一个回测类

from generallib import *
import logging
def configLog():
    # 创建日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # 仅记录 INFO 级别及以上日志

    # 移除所有处理器，防止默认控制台输出
    if logger.hasHandlers():
        logger.handlers.clear()

    # 文件处理器，记录 INFO 级别及以上日志
    file_handler = logging.FileHandler(f'./log/{getToday()}_{getTime()}_futuresBacktesting.log')
    file_handler.setLevel(logging.INFO)  # 忽略 DEBUG 级别
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    # 添加文件处理器到日志记录器
    logger.addHandler(file_handler)

    # 确保日志不会传播到根记录器，防止意外的终端输出
    logger.propagate = False



class Contract:
    # 预定义四种合约状态
    contract_types = ['unlisted', "main", "sub", "currentSeason", "nextSeason", 'expired']

    def __init__(self, code, contract_type='unlisted'):
        self.code = code  # TODO 验证合约代码的合法性，季度合约的代码尾号必须是03, 06, 09, 12
        self.startDate = None
        self.endDate = getContractEndDate(int(code[2:]))
        self.settlementDate = getNextTradeDate(self.endDate)
        self.contract_type = contract_type

        if self.contract_type == "main":
            # 这三种合约计算方法都是一样的
            self.rollOverDate = getMainContractRolloverDate(int(code[2:]))
        elif self.contract_type == "sub":
            self.rollOverDate = getSubContractRolloverDate(int(code[2:]))
        elif self.contract_type == "currentSeason" or self.contract_type == "nextSeason":
            self.rollOverDate = getCurrentAndNextSeasonRolloverDate(int(code[2:]))
        else:
            # raise ValueError(f"Unknown contract type: {self.contract_type}")
            prt.redMsg(f"Bad contract type: {self.contract_type}")
            self.rollOverDate = None

    def __str__(self):
        return f"Contract: [{self.code}]: " \
               f"ends at [{self.endDate}], roll over date is [{self.rollOverDate}]" \
               f", settlement date is [{self.settlementDate}]" \
               f", contract type is [{self.contract_type}]"

    def push_contract_type(self):
        """将合约的类型向右边推进到下一个阶段"""
        current_index = Contract.contract_types.index(self.contract_type)
        if current_index < len(Contract.contract_types) - 1:
            self.contract_type = Contract.contract_types[current_index + 1]
        else:
            raise ValueError("This contract is already at the final type (Next Season).")

    def get_next_contract(self):
        """
        @brief 获取下一个合约
        @return 返回下一个合约对象
        """
        # 提取年份和月份
        year = int(self.code[2:4])  # 取年份的后两位
        month = int(self.code[4:])  # 取月份

        # 根据合约类型更新月份
        if self.contract_type in ["main", "sub"]:
            month += 1  # 下个月
            if month > 12:  # 跨年处理
                month = 1
                year += 1
        elif self.contract_type in ["currentSeason", "nextSeason"]:
            month += 3  # 下个季节合约
            if month > 12:  # 跨年处理
                month -= 12
                year += 1

        # 生成新的合约代码，确保月份两位数格式
        next_code = f"IC{year:02}{month:02}"

        # 创建并返回下一个合约对象
        return Contract(next_code, self.contract_type)


class Trade_futures:
    def __init__(self, contract, start_money, saveDataPath):
        self.contract = contract
        self.startContract = contract
        self.price = 0
        self.quantity = 0
        self.direction = 0
        self.date = None
        self.time = None
        self.start_money = start_money
        self.profit_loss = 0

        self.cash = start_money
        self.current_cash_without_basis = start_money
        self.multiplier = 200  # 合约乘数
        # 保证金费率
        self.margin_rate = 0.12
        # 手续费率
        self.commission_rate = 0.000023

        self.currentCommission = 0
        self.currentDeltaCash = 0
        self.currentMargin = 0
        self.pnl = 0
        self.ZZ500ClosePrice = 0
        

        self.latestPrice = 0  # 这个时候这个合约的最新价

        self.saveDataPath = saveDataPath

        # 如果要增加交易数据，就在这里和 ZFKQQL 处增加列，
        self.transaction = pd.DataFrame(
            columns=['code', 'date', 'time', 'price', 'quantity', 
                     'direction', 'profit_loss', 'current_cash', 'currentCommission', 'currentMargin', 
                     'contract_type', 'ZZ500ClosePrice', 'basis', 'latestPrice', 'marketImpactCost',
                     'current_cash_without_basis'])
        self.asset = pd.DataFrame(
            columns=['date', 'time', 'cash', 'delta'])

    def __str__(self):
        ...

    def trade(self, currentContract, price, quantity, direction, date, time):
        # prt.blackMsg(f'Trade {self.contract.code} at {price} on {date} {time} with {quantity} hand(s)')
        logging.info(f'Trade {currentContract.code} at {price} on {date} {time} with {quantity} hand(s) TRADES')
        self.contract = currentContract

        self.price = price
        self.quantity = quantity
        self.direction = direction
        self.date = date
        self.time = time

        # 有方向的现金流，未计入手续费和保证金费率
        self.currentDeltaCash = self.price * self.quantity * self.multiplier * (1 if self.direction == 1 else -1)

        # 手续费 = 价格 * 数量 * 合约乘数 * 手续费率
        self.currentCommission = self.price * self.quantity * self.multiplier * self.commission_rate

        # 保证金 = 价格 * 数量 * 合约乘数 * 保证金费率 * 方向
        self.currentMargin = self.price * self.quantity * self.multiplier * self.margin_rate * (1 if self.direction == 1 else -1)

        # 现在的现金就是之前的现金减去手续费和保证金
        self.cash -= self.price * self.quantity * self.multiplier * (1 if self.direction == 1 else -1) + self.currentCommission

        # pnl = 价格 * 数量 * 合约乘数 * 方向
        self.pnl = self.calculate_profit_loss(self.price, self.quantity, self.direction)

        # 更新当天的中证500指数收盘价
        self.ZZ500ClosePrice = DataManager().getClosePriceOfZZ500(self.date)

        # 更新# 抹掉基差的current_cash_without_basis
        self.current_cash_without_basis -= self.ZZ500ClosePrice * self.quantity * self.multiplier * (1 if self.direction == 1 else -1) + self.ZZ500ClosePrice * self.quantity * self.multiplier * self.commission_rate

        # 更新最新价
        # TODO 这种方法每次调用时，都会创建一个新的 DataManager 实例，非常消耗资源，上面的也是
        self.latestPrice = DataManager().get_1400_latest_price(self.contract.code, int(self.date))

 


        # print(f"Current Delta Cash: {self.currentDeltaCash}, direction: {self.direction}")
        self.append_transaction()
        # self.append_asset(self.date, self.time)

    def append_transaction(self):
        # ZFKQQL 
        self.transaction = self.transaction.append({
                                'code': self.contract.code,
                                 'date': self.date,
                                 'time': self.time,
                                 'price': self.price,
                                 'quantity': self.quantity,
                                 'direction': self.direction,
                                 'profit_loss': self.pnl,
                                 'current_cash': self.cash,
                                 'currentCommission': self.currentCommission,
                                 'currentMargin': self.currentMargin,
                                 'contract_type': self.contract.contract_type,
                                 'ZZ500ClosePrice': self.ZZ500ClosePrice,
                                 'basis': self.price - self.ZZ500ClosePrice,
                                 'latestPrice': self.latestPrice,
                                 'marketImpactCost': abs((self.price - self.latestPrice)*self.quantity*self.multiplier),
                                 'current_cash_without_basis': self.current_cash_without_basis
                                 }, ignore_index=True)
        # 保存交易数据，文件名是起始的合约代码，不会为了每次换仓而更改
            # 如果没有getDate("")文件夹，就创建一个
        if not os.path.exists(self.saveDataPath + f'\\{getDate("")}'):
            os.makedirs(self.saveDataPath + f'\\{getDate("")}')
        savePathTemp = self.saveDataPath + f'\\{getDate("")}\\{self.startContract.code}_{self.startContract.contract_type}_transaction.csv'
        try:
            self.transaction.to_csv(savePathTemp, index=False)
            appendToListIfNotExists(backtestingResultFileList, savePathTemp)
            # prt.greenMsg(f"Transaction data saved to {savePathTemp} KDVBJK")
        except Exception as e:
            prt.redMsg(f"Error when saving transaction data to {savePathTemp}: {e}")
            

    def append_asset(self, date, time):
        self.asset.append({'date': date,
                           'time': time,

                           }, ignore_index=True)
        savePathTemp = self.saveDataPath + f'\\{self.startContract.code}_{self.startContract.contract_type}_asset.csv'
        try:
            self.asset.to_csv(savePathTemp, index=False)
            prt.greenMsg(f"Asset data saved to {savePathTemp}")
        except Exception as e:
            prt.redMsg(f"Error when saving asset data to {savePathTemp}: {e}")


    def calculate_profit_loss(self, price, quantity, direction):
        abs_profit_loss = abs(price) * quantity * self.multiplier
        if direction == 1:
            return abs_profit_loss
        elif direction == 2:
            return -abs_profit_loss
        else:
            raise ValueError("Direction should be 1 or 2")


class Backtest_futures:
    def __init__(self, contracts: object, start_date: int, end_date: int, vol_at_establishing_position: int):
        '''
        回测会根据合约的类型，自动选择下一个合约进行回测
        入口为 execute 函数
        :param contracts:  合约列表, 也可以是单个合约，例如 [IC2001_MAIN, IC2002_MAIN]，需要是Contract类的实例
        :param start_date: 回测开始日期 yyyyMMdd int
        :param end_date:   回测结束日期 yyyyMMdd int
        :param vol_at_establishing_position: 建仓时的手数,一般为1,不排除有多数量的情况，可能会比较复杂 int
                                             而且，程序是默认在每次换仓的时候，都是以建仓时的手数进行换仓的
        需要注意，如果回测开始日期和结束日期不在合约的交易日期范围内，会提示，然后调整为合约的交易日期范围

        '''
        self.contracts = contracts
        self.start_date = start_date
        self.end_date = end_date
        self.vol_at_establishing_position = vol_at_establishing_position

    def execute(self):
        # 回测的主要逻辑
        for contract in self.contracts:
            prt.magentaMsg(f" -> Executing backtest for contract {contract.code} <-")

            if contract.contract_type == 'unlisted' or contract.contract_type == 'expired':
                prt.yellowMsg(f"This contract is {contract.contract_type}, skip.")
                continue
            else:
                prt.boldMsg(f"This contract is the [{contract.contract_type}] contract, now start backtesting.")
                self.execute_(contract)  # 执行回测

            # print('\n', contract)
            logging.info(backtestingResultFileList)
            prt.greenMsg(f" -> Backtest for contract {contract.code} finished <-")   


    def execute_(self, contract):
        '''
        执行回测
        :return:
        '''
        # 0. 初始化
        dataManager = DataManager()
        tradeSim = Trade_futures(contract, 0, dataPath)  # 交易模拟器, 这个路径是保存路径 PARAS 变量2是初始资金

        # 1. 画图
        # def plot_job():
        #     dataManager.plot_dynamic(tradeSim.transaction, ['current_cash']) # 画图
        # # 创建并启动后台线程
        # plot_thread = threading.Thread(target=plot_job)
        # plot_thread.daemon = True  # 设置为守护线程，当主程序退出时它也会退出
        # plot_thread.start()


        # 2. 建仓
        # 在 contract.startDate 买入 vol_at_establishing_position 手
        logging.info(f"Start date: {contract.startDate}, end date: {contract.endDate}")
        logging.info(f'currentContract is:{contract}')
        actualStartDate = format_dateString_to_YYYYMMDD(getNextTradeDateIfNotTradeDate(get_trade_date(str(self.start_date)[:4]), format_to_datetime(self.start_date)))
        startPrice = dataManager.get_1400_buy_1_price(contract.code, actualStartDate)
        tradeSim.trade(contract, startPrice, 1, 1, actualStartDate, '14:00:00')

        # 3. 第一次换月
        currentContract = contract
        progress_bar = tqdm(total=self.estimate_iterations_for_contract(currentContract) + 1, desc="Backtesting Progress")

        # 条件：当前合约的换仓日期 < 回测的结束日期
        while isDatetimeABeforeB(currentContract.rollOverDate, self.end_date): # GSAXZZ  在回测的结束日期之前执行
            try:
                nextContract = currentContract.get_next_contract()  # 更新下一个合约
                logging.info(f"> Current contract: {currentContract}")
                logging.info(f"> Next contract: {nextContract}")

                # 当前合约平空仓
                # 检查这天140000有没有数据，如果没有就拿150000的今收盘价
                # 以 换仓日 当天1400点的平均买一价 卖出 vol_at_establishing_position 手 currentContract
                tradeSim.trade(
                    currentContract,
                    dataManager.get_1400_sell_1_price(currentContract.code, int(currentContract.rollOverDate.replace('-', ''))),
                    1, 2, currentContract.rollOverDate.replace('-', ''), '14:00:00'
                    )

                # 下一个合约开空仓
                # 同时在当天的 1400 的平均卖一价，买入 vol_at_establishing_position 手 nextContract
                # TODO 特殊的是，如果是最后一次交易，那么上面平仓后，就不再买了
                tradeSim.trade(nextContract,
                    dataManager.get_1400_buy_1_price(nextContract.code, int(currentContract.rollOverDate.replace('-', ''))),
                                1, 1, currentContract.rollOverDate.replace('-', ''), '14:00:00')

                currentContract = nextContract
                logging.info(currentContract)
            except Exception as e:
                prt.redMsg(f"\nError: {e} GDJENM\n"
                           f"at currentRolloverDate {currentContract.rollOverDate}\n原因可能是：\n"
                           f"1. 合约的更换日期不在交易日范围内，请检查\n"
                           f"2. 合约的更换日期不在回测的时间范围内 GSAXZZ\n"
                            f'currentContract is:{currentContract}\n'
                            f'nextContract is:{nextContract}\n'
                            # f'1400 avg sell 1 price is:{dataManager.get_1400_avg_sell_1_price(currentContract.code, int(currentContract.rollOverDate.replace("-", ""))):.2f}\n'
                            # f'1400 avg buy 1 price is:{dataManager.get_1400_avg_buy_1_price(nextContract.code, int(nextContract.rollOverDate.replace("-", ""))):.2f}\n'
                            f'currentContract.rollOverDate is:{currentContract.rollOverDate}\n'
                            f'currentContract.endDate is:{currentContract.endDate}\n'
                            )
                break
            progress_bar.update(1)

        # 4. 平仓
        # 最后一次交易，在 self.end_date 的 14:00:00 平仓, 如果当天不是交易日，就顺延
        actualEndDate = format_dateString_to_YYYYMMDD(getNextTradeDateIfNotTradeDate(get_trade_date(str(self.end_date)[:4]), format_to_datetime(self.end_date)))
        tradeSim.trade(
            currentContract,
            dataManager.get_1400_sell_1_price(currentContract.code, actualEndDate),
            1, 2, actualEndDate, '14:00:00'
        )
        
        progress_bar.close()


    def generate_report(self, preparedCash, backtestingResultFileList, dataPath):
        # 生成报告
        prt.magentaMsg(" -> Generating report <-")

        main_df = pd.DataFrame()
        sub_df = pd.DataFrame()
        currentSeason_df = pd.DataFrame()
        nextSeason_df = pd.DataFrame()

        

        # 1. 读取 backtestingResultFileList 中的所有文件.
        if backtestingResultFileList:
            # 如果文件名里有main，就读取到main_df里，以此类推
            for file in backtestingResultFileList:
                if 'main' in file:
                    main_df = pd.read_csv(file)
                if 'sub' in file:
                    sub_df = pd.read_csv(file)
                if 'currentSeason' in file:
                    currentSeason_df = pd.read_csv(file)
                if 'nextSeason' in file:
                    nextSeason_df = pd.read_csv(file)


        # 2. 如果步骤1中没有数据，就找到当日回测数据，否则输入日期 yyyymmdd 来寻找
        today = getDate('')
        todayDataPath = dataPath + f'\\{today}'
        prt.yellowMsg(f"Today's backtesting data path: {todayDataPath}")
        if os.path.exists(todayDataPath):
            # 读取当日回测数据
            for file in os.listdir(todayDataPath):
                if 'main' in file:
                    main_df = pd.read_csv(todayDataPath + '\\' + file)
                if 'sub' in file:
                    sub_df = pd.read_csv(todayDataPath + '\\' + file)
                if 'currentSeason' in file:
                    currentSeason_df = pd.read_csv(todayDataPath + '\\' + file)
                if 'nextSeason' in file:
                    nextSeason_df = pd.read_csv(todayDataPath + '\\' + file)
        else:
            prt.yellowMsg(f'Today\'s backtesting data path NOT found, input date to find(YYYYMMDD):')
            date = input("")
            otherDataPath = dataPath + f'\\{date}'
            if os.path.exists(otherDataPath):
                # 读取当日回测数据
                for file in os.listdir(otherDataPath):
                    if 'main' in file:
                        main_df = pd.read_csv(otherDataPath + '\\' + file)
                    if 'sub' in file:
                        sub_df = pd.read_csv(otherDataPath + '\\' + file)
                    if 'currentSeason' in file:
                        currentSeason_df = pd.read_csv(otherDataPath + '\\' + file)
                    if 'nextSeason' in file:
                        nextSeason_df = pd.read_csv(otherDataPath + '\\' + file)
            else:
                prt.redMsg(f"Data not found for date {date}, quitting...")
                return 

        dfs = [main_df, sub_df, currentSeason_df, nextSeason_df]

        # 3. 检查和修正数据
        # 检查数据是否为空
        for df in dfs:
            if df.empty:
                prt.redMsg(f"{df}: Data is empty, quitting...")
                prt.yellowMsg(rf"")
                return


        # 如果数据最后一行的 direction 是 1，说明没有平仓，删除这一行数据
        for df in dfs:
            if df.empty:
                continue
            if df.iloc[-1]['direction'] == 1:
                df.drop(df.tail(1).index, inplace=True)
                logging.info(f"Last row deleted in {df} because of direction is 1 GDLFLA")


        # 4. 生成报告
        # 获取每个df最后一行的current_cash,然后比对，看看哪个最大
        main_cash = main_df.iloc[-1]['current_cash']
        sub_cash = sub_df.iloc[-1]['current_cash']
        currentSeason_cash = currentSeason_df.iloc[-1]['current_cash']
        nextSeason_cash = nextSeason_df.iloc[-1]['current_cash']

        # 去掉基差的 current_cash
        main_cash_without_basis = main_df.iloc[-1]['current_cash_without_basis']
        sub_cash_without_basis = sub_df.iloc[-1]['current_cash_without_basis']
        currentSeason_cash_without_basis = currentSeason_df.iloc[-1]['current_cash_without_basis']
        nextSeason_cash_without_basis = nextSeason_df.iloc[-1]['current_cash_without_basis']


        cash_list = [main_cash, sub_cash, currentSeason_cash, nextSeason_cash]

        cash_ratio_list =  [(main_cash+preparedCash)/preparedCash, 
                            (sub_cash+preparedCash)/preparedCash, 
                            (currentSeason_cash+preparedCash)/preparedCash,
                            (nextSeason_cash+preparedCash)/preparedCash]
        
        cash_list_without_basis = [main_cash_without_basis, sub_cash_without_basis, currentSeason_cash_without_basis, nextSeason_cash_without_basis]

        cash_ratio_list_without_basis = [(main_cash_without_basis+preparedCash)/preparedCash, 
                                         (sub_cash_without_basis+preparedCash)/preparedCash, 
                                         (currentSeason_cash_without_basis+preparedCash)/preparedCash, 
                                         (nextSeason_cash_without_basis+preparedCash)/preparedCash]
        
        commission_list = [main_df['currentCommission'].sum(), 
                           sub_df['currentCommission'].sum(), 
                           currentSeason_df['currentCommission'].sum(), 
                           nextSeason_df['currentCommission'].sum()]
        
        impactCost_list = [main_df['marketImpactCost'].sum(), 
                           sub_df['marketImpactCost'].sum(), 
                           currentSeason_df['marketImpactCost'].sum(), 
                           nextSeason_df['marketImpactCost'].sum()]
        
        # 用cash - impactCost来计算排名 (cash里面已经算过了commisiion)
        # 计算每个合约的净收益
        net_profit_list = [cash - impact_cost for cash, impact_cost in zip(cash_list, impactCost_list)]

        # 根据净收益计算排名
        rank_list = sorted(range(len(net_profit_list)), key=lambda x: net_profit_list[x], reverse=True)



        print(f"Main cash: {main_cash}, {cash_ratio_list[0]:.5f} times of prepared cash")
        print(f"Sub cash: {sub_cash}, {cash_ratio_list[1]:.5f} times of prepared cash")
        print(f"Current Season cash: {currentSeason_cash}, {cash_ratio_list[2]:.5f} times of prepared cash")
        print(f"Next Season cash: {nextSeason_cash}, {cash_ratio_list[3]:.5f} times of prepared cash")

        print("")

        print(f"Main cash without basis: {main_cash_without_basis}, {cash_ratio_list_without_basis[0]:.5f} times of prepared cash")
        print(f"Sub cash without basis: {sub_cash_without_basis}, {cash_ratio_list_without_basis[1]:.5f} times of prepared cash")
        print(f"Current Season cash without basis: {currentSeason_cash_without_basis}, {cash_ratio_list_without_basis[2]:.5f} times of prepared cash")
        print(f"Next Season cash without basis: {nextSeason_cash_without_basis}, {cash_ratio_list_without_basis[3]:.5f} times of prepared cash")

        max_cash = max(cash_list)
        max_cash_index = cash_list.index(max_cash)
        prt.greenMsg(f"Max cash is {max_cash}, index is {max_cash_index}")

        # 生成reportDf
        reportDf = pd.DataFrame({
            'Contract Type': ['Main', 'Sub', 'Current Season', 'Next Season'],
            'Cash': cash_list,
            'Cash Ratio': cash_ratio_list,
            'Cash Without Basis': cash_list_without_basis,
            'Cash Ratio Without Basis': cash_ratio_list_without_basis,
            'Commission': commission_list,
            'Impact Cost': impactCost_list,
            'Rank': rank_list
        })
        
        prt.greenMsg("\n==============================================================\n\t\t\t    Report\n")
        print(reportDf)
        prt.greenMsg("\n==============================================================\n")


        # total_profit_loss = sum(trade.profit_loss for trade in self.trades)
        # print(f'Total Profit/Loss: {total_profit_loss}')

        prt.greenMsg(" -> Generating report finished <-")

    def estimate_iterations_for_contract(self, contract: Contract):
        """
        @brief Estimate the number of iterations needed for backtesting based on contract type.
        @param contract, Contract object containing contract type and code.
        @return Estimated number of iterations for backtesting.
        """
        # 结束日期格式 YYYYMMDD, 转换为年和月
        end_year = int(str(self.end_date)[:4])
        end_month = int(str(self.end_date)[4:6])

        # 合约代码格式 IC2001, 解析为年和月
        contract_year = 2000 + int(contract.code[2:4])  # 例如 2001 -> 2020年
        contract_month = int(contract.code[4:])  # 例如 01 -> 1月

        # 根据不同合约类型计算换月频率
        if contract.contract_type == 'main':
            # 每个月换一次
            return (end_year - contract_year) * 12 + (end_month - contract_month)

        if contract.contract_type == 'sub':
            # 假设次主力合约也是每月换一次
            return (end_year - contract_year) * 12 + (end_month - contract_month)

        if contract.contract_type == 'currentSeason':
            # 每个季度换一次（3个月）
            return ((end_year - contract_year) * 12 + (end_month - contract_month)) // 3

        if contract.contract_type == 'nextSeason':
            # 每个季度换一次（3个月），次季节合约
            return ((end_year - contract_year) * 12 + (end_month - contract_month)) // 3

        else:
            raise ValueError("Unknown contract type")


# @brief DataManager负责管理和处理期货数据
# 目前是基于C:\Users\progene12\share\FUTURES_DATA的数据，其数据结构可能具有特殊性，如果换数据源，整个类可能会重写
class DataManager:
    def __init__(self):
        self.dataPath = rf'C:\Users\progene12\share\FUTURES_DATA'  # PARAS
        self.zz500indexPath = rf'D:\lzy\myCode\tradeTools_github\zz500index.csv'  # PARAS


    def getClosePriceOfZZ500(self, date):
        '''
        @brief 获取中证500指数某一天的收盘价
        @param date: str or int, 日期格式为YYYYMMDD

        数据示例
          ,ts_code   ,trade_date ,close     ,open      ,high      ,low       ,pre_close ,change    ,pct_chg ,vol         ,amount
        0 ,000905.SH ,  20241031 ,5901.2904 ,5839.9766 ,5935.1827 ,5812.0324 ,5837.9338 ,63.3566   ,1.0853  ,313549202.0 ,377454102.585
        1 ,000905.SH ,  20241030 ,5837.9338 ,5793.8326 ,5869.1113 ,5777.43   ,5812.5286 ,25.4052   ,0.4371  ,252021275.0 ,315956554.496
        '''
        try:
            # 读取 CSV 文件
            df = pd.read_csv(self.zz500indexPath)

            # 确保日期格式一致
            date = int(date)

            # 过滤指定日期的数据
            row = df[df['trade_date'] == date]
            
            # 检查是否找到对应的行
            if row.empty:
                prt.redMsg(f"Warning: No data found for the specified date: {date}")
                return None

            # 返回收盘价
            close_price = row['close'].values[0]
            return float(close_price)

        except FileNotFoundError:
            prt.redMsg(f"Error: File not found at path {self.zz500indexPath}")
            return None
        except pd.errors.EmptyDataError:
            prt.redMsg("Error: The data file is empty.")
            return None
        except KeyError as e:
            prt.redMsg(f"Error: Missing expected column in data: {e}")
            return None
        except Exception as e:
            prt.redMsg(f"An unexpected error occurred: {e}")
            return None


    @staticmethod
    def get_all_data_for_contract(self, contractName, startDate, endDate):
        '''
        获取这个合约在时间段内的所有数据
        :param self:
        :param contractName:
        :param startDate:
        :param endDate:
        :return:
        '''
        # print(f"Getting data for contract {contractName} from {startDate} to {endDate} YUBNAQ")

    def get_one_day_data_for_contract(self, contractName, date):
        '''
        获取这个合约在某一天的数据
        :param self:
        :param contractName:
        :param date: yyyy-mm-dd
        :return:
        '''
        # 把yyyy-mm-dd格式的日期转换为yyyymmdd
        date = date.replace('-', '')

        # print(f"Getting data for contract {contractName} on {date} LALDSA")
        filePath = rf'{self.dataPath}\{contractName[0:2]}_{date[0:6]}\{contractName}_{date}.csv'
        # print("File Path: ", filePath, 'VJKLZK')
        # file.saveAsUft8(filePath)
        df = pd.read_csv(filePath, encoding='GB2312')
        # 提取 最后修改时间 列为14:00:00的数据
        df_1400 = df[df['最后修改时间'].str.contains('14:00:00')]
        # print(df_1400)

        return df_1400

    def get_1400_avg_buy_1_price(self, contractName: str, date: int) -> float:
        '''
        获取这个合约在某一天的14:00:00的平均买一价，如果14:00:00没有数据，就往后延长一秒，如果一分钟都没有数据，就获取15:00:00的今收盘价
        :param contractName: "IC2001"
        :param date: int 20200102
        :return: float
        '''
        # 确保日期正确格式
        date_with_separator = format_YYYYMMDD_with_separator(str(date), '-')  # str 2020-01-02
        date = str(date)  # str 20200102
        date_with_date_type = format_YYYYMMDD_to_date(date)  # date 2020-01-02
        date = getNextTradeDateIfNotTradeDate(get_trade_date(date[0:4]), date_with_date_type)  # str 20200102
        date = date.replace('-', '')  # str 20200102

        logging.info(f"get_1400_avg_buy_1_price {contractName} on {str(date)} ZXCVJK")
        filePath = rf'{self.dataPath}\{contractName[0:2]}_{date[0:6]}\{contractName}_{date}.csv'
        logging.info(f"File Path: {filePath} CPIGOA")
        logging.info(f"{prt.fileEncoding(filePath)}")

        df = pd.read_csv(filePath, encoding='GB2312')

        try:
            # 尝试提取 14:00:00 到 14:00:59 的数据
            for second in range(60):
                time_str = f'14:00:{second:02d}'
                df_time = df[df['最后修改时间'].str.contains(time_str)]
                if not df_time.empty:
                    avg_order_buy_price_1 = df_time['申买价一'].mean().round(2)
                    return avg_order_buy_price_1
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_avg_buy_1_price  GLPLFS")

        try:
            # 如果没有14:00数据，检查15:00:00的‘今收盘’
            df_1500 = df[df['最后修改时间'].str.contains('15:00:00')]
            if not df_1500.empty:
                last_close_price = df_1500['今收盘'].values[0]
                if last_close_price == 0:
                    raise ValueError(f"Error: No valid '今收盘' for contract {contractName} on {date}")
                return last_close_price
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_avg_buy_1_price  GLPLFD")

        raise ValueError(f"No data for 14:00:00 or 15:00:00 on {date} for {contractName}")

    def get_1400_avg_sell_1_price(self, contractName: str, date: int) -> float:
        '''
        获取这个合约在某一天的14:00:00的平均卖一价，如果14:00:00没有数据，获取15:00:00的今收盘价
        :param contractName: "IC2001"
        :param date: int 20200102
        :return: float
        '''
        # 确保日期正确格式
        date_with_separator = format_YYYYMMDD_with_separator(str(date), '-')  # str 2020-01-02
        date = str(date)  # str 20200102
        date_with_date_type = format_YYYYMMDD_to_date(date)  # date 2020-01-02
        date = getNextTradeDateIfNotTradeDate(get_trade_date(date[0:4]), date_with_date_type)  # str 20200102
        date = date.replace('-', '')  # str 20200102

        logging.info(f"get_1400_avg_sell_1_price {contractName} on {str(date)} ALQQQQ")
        filePath = rf'{self.dataPath}\{contractName[0:2]}_{date[0:6]}\{contractName}_{date}.csv'
        logging.info(f"File Path: {filePath} ASFKJV")
        # prt.fileEncoding(filePath)
        logging.info(f"{prt.fileEncoding(filePath)}")

        df = pd.read_csv(filePath, encoding='GB2312')

        try:
            # 尝试提取 14:00:00 到 14:00:59 的数据
            for second in range(60):
                time_str = f'14:00:{second:02d}'
                df_time = df[df['最后修改时间'].str.contains(time_str)]
                if not df_time.empty:
                    avg_order_sell_price_1 = df_time['申卖价一'].mean().round(2)
                    return avg_order_sell_price_1
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_avg_sell_1_price  ZXZNMR")

        try:
            # 如果没有14:00数据，检查15:00:00的‘今收盘’
            df_1500 = df[df['最后修改时间'].str.contains('15:00:00')]
            if not df_1500.empty:
                last_close_price = df_1500['今收盘'].values[0]
                if last_close_price == 0:
                    raise ValueError(f"Error: No valid '今收盘' for contract {contractName} on {date}")
                return last_close_price
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_avg_sell_1_price  GLADZZ")

        raise ValueError(f"No data for 14:00:00 or 15:00:00 on {date} for {contractName}")

    def get_1400_buy_1_price(self, contractName: str, date: int) -> float:
        '''
        获取这个合约在某一天的14:00:00的精确买一价，如果14:00:00没有数据，就往后延长一秒，如果一分钟都没有数据，就获取15:00:00的今收盘价
        :param contractName: "IC2001"
        :param date: int 20200102
        :return: float
        '''
        # 确保日期正确格式
        date_with_separator = format_YYYYMMDD_with_separator(str(date), '-')  # str 2020-01-02
        date = str(date)  # str 20200102
        date_with_date_type = format_YYYYMMDD_to_date(date)  # date 2020-01-02
        date = getNextTradeDateIfNotTradeDate(get_trade_date(date[0:4]), date_with_date_type)  # str 20200102
        date = date.replace('-', '')  # str 20200102

        logging.info(f"get_1400_buy_1_price {contractName} on {str(date)}")
        filePath = rf'{self.dataPath}\{contractName[0:2]}_{date[0:6]}\{contractName}_{date}.csv'
        logging.info(f"File Path: {filePath}")
        logging.info(f"{prt.fileEncoding(filePath)}")

        df = pd.read_csv(filePath, encoding='GB2312', low_memory=False)

        try:
            # 尝试提取 14:00:00 到 14:00:59 的数据
            for second in range(60):
                time_str = f'14:00:{second:02d}'
                df_time = df[df['最后修改时间'].str.contains(time_str)]
                if not df_time.empty:
                    return df_time['申买价一'].values[0]
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_buy_1_price VKZLXK")

        try:
            # 如果没有14:00数据，检查15:00:00的‘今收盘’
            df_1500 = df[df['最后修改时间'].str.contains('15:00:00')]
            if not df_1500.empty:
                last_close_price = df_1500['今收盘'].values[0]
                if last_close_price == 0:
                    raise ValueError(f"Error: No valid '今收盘' for contract {contractName} on {date}")
                return last_close_price
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_buy_1_price  GLPASA")

        raise ValueError(f"No data for 14:00:00 or 15:00:00 on {date} for {contractName}")

    def get_1400_sell_1_price(self, contractName: str, date: int) -> float:
        '''
        获取这个合约在某一天的14:00:00的精确卖一价，如果14:00:00没有数据，获取15:00:00的今收盘价
        :param contractName: "IC2001"
        :param date: int 20200102
        :return: float
        '''
        # 确保日期正确格式
        date_with_separator = format_YYYYMMDD_with_separator(str(date), '-')  # str 2020-01-02
        date = str(date)  # str 20200102
        date_with_date_type = format_YYYYMMDD_to_date(date)  # date 2020-01-02
        date = getNextTradeDateIfNotTradeDate(get_trade_date(date[0:4]), date_with_date_type)  # str 20200102
        date = date.replace('-', '')  # str 20200102

        logging.info(f"get_1400_sell_1_price {contractName} on {str(date)}")
        filePath = rf'{self.dataPath}\{contractName[0:2]}_{date[0:6]}\{contractName}_{date}.csv'
        logging.info(f"File Path: {filePath}")
        logging.info(f"{prt.fileEncoding(filePath)}")

        df = pd.read_csv(filePath, encoding='GB2312', low_memory=False)

        try:
            # 尝试提取 14:00:00 到 14:00:59 的数据
            for second in range(60):
                time_str = f'14:00:{second:02d}'
                df_time = df[df['最后修改时间'].str.contains(time_str)]
                if not df_time.empty:
                    return df_time['申卖价一'].values[0]
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_sell_1_price  ZBGGQW")

        try:
            # 如果没有14:00数据，检查15:00:00的‘今收盘’
            df_1500 = df[df['最后修改时间'].str.contains('15:00:00')]
            if not df_1500.empty:
                last_close_price = df_1500['今收盘'].values[0]
                if last_close_price == 0:
                    raise ValueError(f"Error: No valid '今收盘' for contract {contractName} on {date}")
                return last_close_price
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_sell_1_price  SASASD")
        raise ValueError(f"No data for 14:00:00 or 15:00:00 on {date} for {contractName}")

    def get_1400_latest_price(self, contractName: str, date: int) -> float:
        '''
        获取这个合约在某一天的14:00:00的最新价，如果14:00:00没有数据，获取15:00:00的今收盘价
        :param contractName: "IC2001"
        :param date: int 20200102
        :return: float
        '''
        # 确保日期正确格式
        date_with_separator = format_YYYYMMDD_with_separator(str(date), '-')  # str 2020-01-02
        date = str(date)  # str 20200102
        date_with_date_type = format_YYYYMMDD_to_date(date)  # date 2020-01-02
        date = getNextTradeDateIfNotTradeDate(get_trade_date(date[0:4]), date_with_date_type)  # str 20200102
        date = date.replace('-', '')  # str 20200102

        logging.info(f"get_1400_latest_price {contractName} on {str(date)}")
        filePath = rf'{self.dataPath}\{contractName[0:2]}_{date[0:6]}\{contractName}_{date}.csv'
        logging.info(f"File Path: {filePath}")
        logging.info(f"{prt.fileEncoding(filePath)}")

        df = pd.read_csv(filePath, encoding='GB2312', low_memory=False)

        try:
            # 尝试提取 14:00:00 到 14:00:59 的数据
            for second in range(60):
                time_str = f'14:00:{second:02d}'
                df_time = df[df['最后修改时间'].str.contains(time_str)]
                if not df_time.empty:
                    return df_time['最新价'].values[0]
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_latest_price ZBGGQW")

        try:
            # 如果没有14:00数据，检查15:00:00的‘今收盘’
            df_1500 = df[df['最后修改时间'].str.contains('15:00:00')]
            if not df_1500.empty:
                last_close_price = df_1500['今收盘'].values[0]
                if last_close_price == 0:
                    raise ValueError(f"Error: No valid '今收盘' for contract {contractName} on {date}")
                return last_close_price
        except Exception as e:
            logging.error(f"Error: {e} in get_1400_latest_price SASASD")
        
        raise ValueError(f"No data for 14:00:00 or 15:00:00 on {date} for {contractName}")
        


    # @brief 动态更新图像
    # @param df 传入的数据，包含日期和目标列
    # @param target_columns 需要绘制的列，可以是一个或两个
    # @param interval 刷新间隔时间（以毫秒为单位），默认为5000ms
    # @return 动态更新的图像
    # plot_dynamic(df, ['col1', 'col2'])
    @staticmethod
    # def draw_plot_in_thread(df, target_columns, interval=3000):
    def plot_dynamic(df, target_columns, interval=3000):

        # 保证target_columns为列表形式
        if isinstance(target_columns, str):
            target_columns = [target_columns]

        # 初始化绘图
        fig, ax = plt.subplots()

        def update(frame):
            ax.clear()  # 清空当前的绘图
            ax.set_xlabel("Date")
            ax.set_ylabel("Value")
            ax.set_title("Dynamic Plot")

            for col in target_columns:
                ax.plot(df['date'], df[col], label=col)

            ax.legend()
            ax.tick_params(axis='x', rotation=45)  # 旋转x轴刻度

        ani = FuncAnimation(fig, update, interval=interval)
        plt.show()

    def get_end_of_data_date(self):
        '''
        获取数据的最后一天
        :return:
        '''
        ...
