import json
import time
import os
from collections import OrderedDict

if __name__ == "__main__":
    print os.path.abspath(__file__)
    # with open(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', 'res1.json')), 'r') as f:
    k=1
    total_instr = 0
    balance_archived = 0
    balance_profit = 0
    balance_loss = 0
    balance_archive_profit = {}
    balance_archive_loss = {}
    while k< 9:
        data = json.load(open(os.path.abspath(os.path.join(os.path.abspath(__file__), '..', 'res'+str(k)+'.json'))), object_pairs_hook=OrderedDict)
        #data={tool0:{day0:{time:[param0... paramN]... timeN:[param0... paramN]}}}
        k +=1
        logs = {}
        cyrillic_translit = {u'\u0410': 'A', u'\u0430': 'a',
                             u'\u0411': 'B', u'\u0431': 'b',
                             u'\u0412': 'V', u'\u0432': 'v',
                             u'\u0413': 'G', u'\u0433': 'g',
                             u'\u0414': 'D', u'\u0434': 'd',
                             u'\u0415': 'E', u'\u0435': 'e',
                             u'\u0416': 'Zh', u'\u0436': 'zh',
                             u'\u0417': 'Z', u'\u0437': 'z',
                             u'\u0418': 'I', u'\u0438': 'i',
                             u'\u0419': 'I', u'\u0439': 'i',
                             u'\u041a': 'K', u'\u043a': 'k',
                             u'\u041b': 'L', u'\u043b': 'l',
                             u'\u041c': 'M', u'\u043c': 'm',
                             u'\u041d': 'N', u'\u043d': 'n',
                             u'\u041e': 'O', u'\u043e': 'o',
                             u'\u041f': 'P', u'\u043f': 'p',
                             u'\u0420': 'R', u'\u0440': 'r',
                             u'\u0421': 'S', u'\u0441': 's',
                             u'\u0422': 'T', u'\u0442': 't',
                             u'\u0423': 'U', u'\u0443': 'u',
                             u'\u0424': 'F', u'\u0444': 'f',
                             u'\u0425': 'Kh', u'\u0445': 'kh',
                             u'\u0426': 'Ts', u'\u0446': 'ts',
                             u'\u0427': 'Ch', u'\u0447': 'ch',
                             u'\u0428': 'Sh', u'\u0448': 'sh',
                             u'\u0429': 'Shch', u'\u0449': 'shch',
                             u'\u042a': '"', u'\u044a': '"',
                             u'\u042b': 'Y', u'\u044b': 'y',
                             u'\u042c': "'", u'\u044c': "'",
                             u'\u042d': 'E', u'\u044d': 'e',
                             u'\u042e': 'Iu', u'\u044e': 'iu',
                             u'\u042f': 'Ia', u'\u044f': 'ia'}
        # print data
        total_balance = 0
        for tool in data:
            total_instr +=1

            translit_name = ''
            for letter in tool:
                if cyrillic_translit.get(letter):
                    translit_name += cyrillic_translit[letter]
                else:
                    translit_name += letter
            print translit_name
            logs[translit_name] = {'balance':0,
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

            i = 0
            while i< len(days)-1:
                hours_thisday = data[tool][days[i + 1]].keys()
                hours_prevday = data[tool][days[i]].keys()
                #checking close of '1' hour of the day and low of 0 hour
                print data[tool][days[i + 1]]

                if len(data[tool][days[i+1]].keys()) > 2 and float(data[tool][days[i+1]][hours_thisday[1]][3]) >= float(data[tool][days[i+1]][hours_thisday[0]][2]) and float(data[tool][days[i+1]][hours_thisday[1]][4]) < float(data[tool][days[i+1]][hours_thisday[0]][4]):
                    if float(data[tool][days[i+1]][hours_thisday[1]][4]) > float(data[tool][days[i]][hours_prevday[-1]][4]) and float(data[tool][days[i+1]][hours_thisday[0]][3]) < float(data[tool][days[i]][hours_prevday[-1]][3]):
                        bid = float(data[tool][days[i + 1]][hours_thisday[1]][0])

                        stoploss = None
                        if float(data[tool][days[i + 1]][hours_thisday[1]][3]) > float(data[tool][days[i+1]][hours_thisday[1]][2]):
                            stoploss = float(data[tool][days[i+1]][hours_thisday[1]][2]) - 0.001 * float(data[tool][days[i+1]][hours_thisday[1]][2])
                        else:
                            stoploss = float(data[tool][days[i+1]][hours_thisday[1]][3]) - 0.003 * float(data[tool][days[i+1]][hours_thisday[1]][3])

                        j = 3
                        while j< len(hours_thisday):
                            hour_low = float(data[tool][days[i + 1]][hours_thisday[j]][2])
                            hour_close = float(data[tool][days[i + 1]][hours_thisday[j]][3])
                            if hour_low <= stoploss:
                                closed_stoploss[days[i+1]] = stoploss - bid

                            if j+1 == len(hours_thisday):
                                #profit
                                if hour_close > bid:
                                    closed_profit[days[i+1]] = hour_close - bid
                                elif hour_close == bid:
                                    closed_noprofit[days[i+1]] = 0
                                elif hour_close < bid:
                                    closed_loss[days[i+1]] = hour_close - bid
                            j+=1
                i += 1
            print "Profit", closed_profit
            print "Loss", closed_loss
            print "Stoploss", closed_stoploss
            print "NoProfit", closed_noprofit

            balance = 0
            for day in closed_profit:
                balance += closed_profit[day]
            for day in closed_loss:
                balance += closed_loss[day]
            for day in closed_stoploss:
                balance += closed_stoploss[day]
            if balance > 1:
                balance_archive_profit[translit_name] = balance
                balance_profit += balance
            else:
                balance_archive_loss[translit_name] = balance
                balance_loss += balance
                # balance_archived = balance
            total_balance += balance
            logs[translit_name] = {'balance': balance,
                          'days_profit': len(closed_profit.keys()),
                          'days_loss': {
                              'days_stoploss': len(closed_stoploss.keys()),
                              'days_timeloss': len(closed_loss.keys()),
                          },
                          'days_noprofit': len(closed_noprofit.keys()),
                          }

            print logs
    closedby_stoploss_total_days= 0
    closedby_time_profit_total_days=0
    closedby_time_noprofit_total_days=0
    closedby_time_loss_total_days = 0
    for instr in logs:
        closedby_stoploss_total_days += logs[instr]['days_loss']['days_stoploss']
        closedby_time_profit_total_days += logs[instr]['days_profit']
        closedby_time_noprofit_total_days += logs[instr]['days_noprofit']
        closedby_time_loss_total_days += logs[instr]['days_loss']['days_timeloss']
    logs['total'] = {'closedby_stoploss_total_days':closedby_stoploss_total_days,
                    'closedby_time_profit_total_days':closedby_time_profit_total_days,
                    'closedby_time_noprofit_total_days':closedby_time_noprofit_total_days,
                    'closedby_time_loss_total_days':closedby_time_loss_total_days,
                    'profit_vs_loss': balance_profit / balance_loss}
    logs['instruments_total'] = total_instr
    logs['instruments_best'] = balance_archive_profit
    logs['instruments_best_quantity'] = len(balance_archive_profit)
    logs['instruments_worst'] = balance_archive_loss
    logs['instruments_worst_quantity'] = len(balance_archive_loss)
    logs['deals_profit_vs_loss'] =float(len(balance_archive_profit.keys())) / float(len(balance_archive_loss.keys()))

    with open('logs.json', 'a') as f:
        f.write(json.dumps(logs, sort_keys=True))
    #data_return = {tool0:{stopLossClosedDays:st_days,
                #          timeWinDays:tmw_days,
                #          timeNoProfitDays: tmnp_days,
                #          timeLoseDays: tml_days,
                #          winVsLoose: tmw_days / tml_days,
                #
                # }