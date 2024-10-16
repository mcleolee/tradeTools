from generallib import *

prt.headlineMsg("THIS IS A FUTURE BACKTESTING SOFTWARE")


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
               f"\nends at [{self.endDate}], roll over date is [{self.rollOverDate}]" \
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


class Trade:
    def __init__(self, contract, price, quantity, direction, date, time, start_money):
        self.contract = contract
        self.price = price
        self.quantity = quantity
        self.direction = direction
        self.date = date
        self.time = time
        self.start_money = start_money
        self.profit_loss = self.calculate_profit_loss()
        self.transaction = pd.DataFrame(columns=['code', 'date', 'time', 'price', 'quantity', 'direction', 'profit_loss', 'contract_type'])
        self.asset = pd.DataFrame(columns=['cash', 'delta'])

    def __str__(self):
        ...

    def trade(self):
        ...

    def append_transaction(self, price, quantity):
        self.transaction.append({}, ignore_index=True)

    def append_asset(self, date, asset):
        self.asset.append({'date': date , 'asset': asset}, ignore_index=True)



    def calculate_profit_loss(self):
        ...
        # return (self.exit_price - self.entry_price) * self.quantity


class Backtest:
    def __init__(self, contracts: object, start_date: int, end_date: int, vol_at_establishing_position: int):
        '''
        回测会根据合约的类型，自动选择下一个合约进行回测
        入口为 execute 函数
        :param contracts:  合约列表, 也可以是单个合约，例如 [IC2001_MAIN, IC2002_MAIN]，需要是Contract类的实例
        :param start_date: 回测开始日期 yyyyMMdd int
        :param end_date:   回测结束日期 yyyyMMdd int
        :param vol_at_establishing_position: 建仓时的手数,一般为1,不排除有多数量的情况，可能会比较复杂 int
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
                self.execute_(contract) # 执行回测

            print('\n', contract)


    def execute_(self, contract):
        '''
        执行回测
        :return:
        '''
        # 0. 初始化
        dm = DataManager()

        # 1. 建仓
        # 在 contract.startDate 买入 vol_at_establishing_position 手
        dm.get_1400_avg_buy_1_price(contract.code, self.start_date)
        # trade = Trade(contract, dm.get_1400_avg_buy_1_price(contract.code, self.start_date), self.vol_at_establishing_position, 'buy', contract.startDate, '14:00:00', 10000000)



        # 读取数据

        df_1400 = dm.get_one_day_data_for_contract(contract.code, contract.rollOverDate)

        avg_order_buy_price_1 = df_1400['申买价一'].mean().round(2)
        avg_order_buy_volume_1 = df_1400['申买量一'].mean().round(0)
        avg_order_sell_price_1 = df_1400['申卖价一'].mean().round(2)
        avg_order_sell_volume_1 = df_1400['申卖量一'].mean().round(0)
        current_price = df_1400['最新价'].mean().round(2)

        prt.blueMsg(
            f"Current Price: [{current_price}], Average Order Buy Price 1: [{avg_order_buy_price_1}], Average Order Buy Volume 1: [{avg_order_buy_volume_1}], Average Order Sell Price 1: [{avg_order_sell_price_1}], Average Order Sell Volume 1:[{avg_order_sell_volume_1}]")




    def generate_report(self):
        total_profit_loss = sum(trade.profit_loss for trade in self.trades)
        print(f'Total Profit/Loss: {total_profit_loss}')



# @brief DataManager负责管理和处理期货数据
# 目前是基于C:\Users\progene12\share\FUTURES_DATA的数据，其数据结构可能具有特殊性，如果换数据源，整个类可能会重写
class DataManager:
    def __init__(self):
        self.dataPath = rf'C:\Users\progene12\share\FUTURES_DATA'

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
        print(f"Getting data for contract {contractName} from {startDate} to {endDate}")

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

        print(f"Getting data for contract {contractName} on {date}")
        filePath = rf'{self.dataPath}\{contractName[0:2]}_{date[0:6]}\{contractName}_{date}.csv'
        print("File Path: ", filePath)
        file.saveAsUft8(filePath)
        df = pd.read_csv(filePath)
        # 提取 最后修改时间 列为14:00:00的数据
        df_1400 = df[df['最后修改时间'].str.contains('14:00:00')]
        # print(df_1400)

        return df_1400

    def get_1400_avg_buy_1_price(self, contractName: str, date: int) -> float:
        '''
        获取这个合约在某一天的14:00:00的平均买一价
        :param contractName: "IC2001"
        :param date: int 20200102
        :return:float
        '''

        # 下面这段代码是为了确保date是交易日，并把传入的int类型的日期转换为正确str类型的日期
        date_with_separator = format_YYYYMMDD_with_separator(str(date), '-') # str 2020-01-02
        date = str(date) # str 20200102
        date_with_date_type = format_YYYYMMDD_to_date(date) # date 2020-01-02
        date = getNextTradeDateIfNotTradeDate(get_trade_date(date[0:4]), date_with_date_type) # str 20200102
        date = date.replace('-', '') # str 20200102

        print(f"Getting data for contract {contractName} on {date}")
        # 应是 "C:\Users\progene12\share\FUTURES_DATA\IC_202001\IC2001_20200102.csv"
        filePath = rf'{self.dataPath}\{contractName[0:2]}_{date[0:6]}\{contractName}_{date}.csv'
        print("File Path: ", filePath)
        file.saveAsUft8(filePath)
        df = pd.read_csv(filePath)
        # 提取 最后修改时间 列为14:00:00的数据
        df_1400 = df[df['最后修改时间'].str.contains('14:00:00')]
        avg_order_buy_price_1 = df_1400['申买价一'].mean().round(2)

        return avg_order_buy_price_1

    def get_1400_avg_sell_1_price(self, contractName: str, date: int) -> float:
        # 下面这段代码是为了确保date是交易日，并把传入的int类型的日期转换为正确str类型的日期
        date_with_separator = format_YYYYMMDD_with_separator(str(date), '-') # str 2020-01-02
        date = str(date) # str 20200102
        date_with_date_type = format_YYYYMMDD_to_date(date) # date 2020-01-02
        date = getNextTradeDateIfNotTradeDate(get_trade_date(date[0:4]), date_with_date_type) # str 20200102
        date = date.replace('-', '') # str 20200102


        print(f"Getting data for contract {contractName} on {date}")
        filePath = rf'{self.dataPath}\{contractName[0:2]}_{date[0:6]}\{contractName}_{date}.csv'
        print("File Path: ", filePath)
        file.saveAsUft8(filePath)
        df = pd.read_csv(filePath)
        # 提取 最后修改时间 列为14:00:00的数据
        df_1400 = df[df['最后修改时间'].str.contains('14:00:00')]
        avg_order_sell_price_1 = df_1400['申卖价一'].mean().round(2)

        return avg_order_sell_price_1



# 动态生成合约并赋予变量名
def create_next_contracts(initial_contract, num_contracts):
    current_contract = initial_contract
    for i in range(num_contracts):
        # 动态生成变量名，例如 IC2101_MAIN, IC2102_MAIN
        globals()[f"{current_contract.code}_{current_contract.contract_type.upper()}"] = current_contract
        print(f"Created contract: {current_contract.code}_{current_contract.contract_type.upper()}")

        # 生成下一个合约
        current_contract = current_contract.get_next_contract()


if __name__ == '__main__':
    IC2001_MAIN = Contract("IC2001", "main")
    IC2002_SUB = Contract("IC2002", "sub")
    IC2003_CURRENTSEASON = Contract("IC2003", "currentSeason")
    IC2006_NEXTSEASON = Contract("IC2006", "nextSeason")

    backtest = Backtest([IC2001_MAIN], 20200101, 20241012, 1)
    backtest.execute()

    IC2001_MAIN.get_next_contract()
    # print(IC2102_MAIN)
    # backtest.contracts.append(IC2102_MAIN)
    # backtest.execute()


