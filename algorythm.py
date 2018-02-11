import json
import time
import os

if __name__ == "__main__":
    print os.path.abspath(__file__)
    with open(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', 'res1.json')), 'r') as f:
        data = json.loads(f.read())
    #data={tool0:{day0:{time:[param0... paramN]... timeN:[param0... paramN]}}}

    logs = {}
    print data
    time.sleep(10)
    i= 0
    for tool in data:

        logs[tool] = {'balance':0,
                      'days_profit':0,
                        'days_loss':{
                                    'days_stoploss':0,
                                    'days_timeloss':0,
                                    },
                        'days_noprofit':0,

        }
        days = data[tool].keys()
        # for day in data[tool]:
        closed_profit = {}
        closed_loss = {}
        closed_stoploss = {}
        closed_noprofit = {}
        bid = None
        while i< len(days)-1:
            hours_thisday = data[tool][days[i + 1]].keys()
            hours_prevday = data[tool][days[i]].keys()
            #checking close of '1' hour of the day and low of 0 hour
            if float(data[tool][days[i+1]][hours_thisday[1]][3]) >= float(data[tool][days[i+1]][hours_thisday[0]][2]) and float(data[tool][days[i+1]][hours_thisday[1]][4]) < float(data[tool][days[i+1]][hours_thisday[0]][4]):
                if float(data[tool][days[i+1]][hours_thisday[1]][4]) >= float(data[tool][days[i]][hours_prevday[:-1]][4]) and float(data[tool][days[i+1]][hours_thisday[0]][3]) < float(data[tool][days[i]][hours_prevday[:-1]][3]):
                    bid = float([data[tool][days[i + 1]][hours_thisday[1]][0]])
                    stoploss = None
                    if float(data[tool][days[i + 1]][hours_thisday[1]][3]) > float(data[tool][days[i+1]][hours_thisday[1]][2]):
                        stoploss = float(data[tool][days[i+1]][hours_thisday[1]][2]) - 0,001 * float(data[tool][days[i+1]][hours_thisday[1]][2])
                    else:
                        stoploss = float(data[tool][days[i+1]][hours_thisday[1]][3]) - 0,003 * float(data[tool][days[i+1]][hours_thisday[1]][3])
                    j = 3
                    while j< len(hours_thisday):
                        hour_low = float(data[tool][days[i + 1]][hours_thisday[j]][2])
                        hour_close = float(data[tool][days[i + 1]][hours_thisday[j]][3])
                        if hour_low <= stoploss:
                            closed_stoploss[days[i+1]] = (stoploss - bid)

                        if j+1 == len(hours_thisday):
                            #profit
                            if hour_close > bid:
                                closed_profit[days[i+1]] = hour_close - bid
                            elif hour_close == bid:
                                closed_noprofit[days[i+1]] = 0
                            elif hour_close < bid:
                                closed_loss[days[i+1]] = hour_close - bid
                        j+=1
        balance = 0
        for day in closed_profit:
            balance += closed_profit[day]
        for day in closed_loss:
            balance += closed_loss[day]
        for day in closed_stoploss:
            balance += closed_stoploss[day]
        logs[tool] = {'balance': balance,
                      'days_profit': len(closed_profit.keys()),
                      'days_loss': {
                          'days_stoploss': len(closed_stoploss.keys()),
                          'days_timeloss': len(closed_loss.keys()),
                      },
                      'days_noprofit': len(closed_noprofit.keys()),

                      }
        print logs
    with open('logs.json', 'w+') as f:
        f.write(json.dumps(logs, sort_keys=True))
    #data_return = {tool0:{stopLossClosedDays:st_days,
                #          timeWinDays:tmw_days,
                #          timeNoProfitDays: tmnp_days,
                #          timeLoseDays: tml_days,
                #          winVsLoose: tmw_days / tml_days,
                #
                # }