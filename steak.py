shipping = 25

# 牛排单价（每100g）
prices_per_100g = {
    "T bone": 18,
    "sirloin": 15,
    "Rump": 16,
    "Chunk tender": 11,
    "lamp chops": 13,
    "filet": 18,
    "ribeye": 16.4
}

# 每块肉的大概重量（g）
weights = {
    "T bone": 800,
    "sirloin": 233.5,
    "Rump": 307,
    "Chunk tender": 200,
    "lamp chops": 95,
    "filet": 160,
    "ribeye": 301.5
}

def calculate_total_price(order):
    total_price = 0
    for steak, quantity in order.items():
        if steak in prices_per_100g:
            weight = weights[steak]
            price_per_piece = (weight / 100) * prices_per_100g[steak]
            total_price += price_per_piece * quantity
        else:
            print(f"未知牛排类型: {steak}")
    return total_price

# 输入每种牛排的数量
order = {
    "T bone": 0,        # 有点硬，不好吃     6
    "sirloin": 2,       # 可以再试试        8
    "Rump": 3,          # 好吃              9
    "Chunk tender": 1,  # 没有肥肉          7
    "lamp chops": 10,    # 喜欢              10
    "filet": 1,         # 挺嫩的            7
    "ribeye": 1         # 太大坨，不好吃     6
}

total_price = calculate_total_price(order)
# 清屏
print("\t\033c")
print("\t", "-" * 38)
# 打印绿色粗体下划线的STEAK Bill
print("\t\t       \033[1;32;4mSTEAK Bill\033[0m")
print("\t", "-" * 38)
# 输出每种牛排的单价和总价
for steak, quantity in order.items():
    if steak in prices_per_100g:
        weight = weights[steak]
        price_per_piece = (weight / 100) * prices_per_100g[steak]
        total_price_for_steak = price_per_piece * quantity
        print("\t", f"{steak: <15}: ¥{price_per_piece:.2f} x {quantity: <2} = ¥{total_price_for_steak:.2f}")
    else:
        print(f"未知牛排类型: {steak}")
print("\t", "-" * 38)
print("\t", f"Total Steak: {'¥':>19}{total_price:.2f}")
print("\t", f"Shipping: {'¥':>22}{shipping:.2f}")
print("\t", "-" * 38)
print("\t", f"Total Price {'¥':>20}{total_price + shipping:.2f}")
print("\n\n\n")


# 1 ribeye 301g.  49rmb 
# 1 filet  150g. 27rmb 
# 1 rump 170g 27.2rmb
# 1 sirloin 232g. 34.8rmb 
# 1 chuck 156g. 17.16rmb
# 2 lamb chops 186g. 24.18rmb 
# Delivery: 23rmb 
# Total: 202rmb

# 10个羊排 974g  97.4
# 3块rump 922g  307
# 2块西冷 467g  233.5
# 1块嫩肩肉 139g    139 
# 1块菲力 163g  163 
# 1块眼肉 302g  302
# 快递：22元

# Total: 459元 
