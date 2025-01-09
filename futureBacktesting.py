from generallib import *
import logging

from backtest import *

# prt.headlineMsg("THIS IS A FUTURE BACKTESTING SOFTWARE")

dataPath = rf'D:\lzy\myCode\tradeTools_github\futureBacktestingResult'
backtestingResultFileList = []



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
    logging.info(" == Start backtesting == ")
    configLog()
    os.system('cls')
    
    IC2001_MAIN = Contract("IC2001", "main")  
    IC2002_SUB = Contract("IC2002", "sub")
    IC2003_CURRENTSEASON = Contract("IC2003", "currentSeason")
    IC2006_NEXTSEASON = Contract("IC2006", "nextSeason")

    # backtest = Backtest([IC2001_MAIN], 20200101, 20241012, 1)
    # backtest = Backtest([IC2003_CURRENTSEASON], 20200101, 20240831, 1)
    backtest = Backtest_futures([IC2001_MAIN, IC2002_SUB, IC2003_CURRENTSEASON, IC2006_NEXTSEASON], 20200101, 20240831, 1) # TODO 这里的[IC2001_MAIN]中的2001要和20200101的年份月份对应，不然会报错
    
    # backtest.execute()
    backtest.generate_report(1000000, backtestingResultFileList, dataPath)  # 传入初始资金

    




