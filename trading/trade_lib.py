# 본인은 비트코인과 이더리움만 매매 할 것이므로.
price_dic={
    "btc":[100,200,300,400],
    "eth":[200,300,400,500]
}

# 구입할 가격
def open_price(asset_type):
    if asset_type not in price_dic.keys():
        print("존재하지 않는 자산입니다.")
        exit(0)
    return price_dic[asset_type][0]

# 손절할 가격
def close_price(asset_type):
    if asset_type not in price_dic.keys():
        print("존재하지 않는 자산입니다.")
        exit(0)
    return price_dic[asset_type][3]