import yfinance as yf
import random
import pandas as pd
import statistics
from before_request import check_redis_key,set_redis_key
import json
from flask import request, jsonify
from common import logging
import constants
avg1 = []
med1=[]
avg2=[]
med2=[]
avg3 = []
med3 = []
valuation_measures = constants.valuation_measures
gr_1 = constants.gr_1
gr_2 = constants.gr_2
gr_3 = constants.gr_3


def average(lst):
   return sum(lst) / len(lst)


def filter_dict(original_dict, keys_to_extract):
   return {key: original_dict[key] for key in keys_to_extract if key in original_dict}


all = []
def group_wise_calculations(symbols_list, perc, discount):
    valuation_data = {}
    total_ev_ebidta = 0
    total_ent_rev = 0
    total_p_e = 0
    tot = 0
    medev = []
    medrev = []
    medpe = []
    for ticker in symbols_list:
        try:
            x = check_redis_key(ticker)
            if x is None:
                try:
                    company = yf.Ticker(ticker)
                    logging.info(f'fetched ticker {company} successfully')
                    if not company.info:
                        logging.warning(f'No data found for ticker {ticker}')
                        continue  # Skip this ticker
                except:
                    logging.error('Failed to fetch')
                try:
                    company_info = company.info  # Extract the dictionary containing company data
                    set_redis_key(ticker, json.dumps(company_info), ttl=86400)
                    logging.info('Ticker stored in Redis')
                except Exception as e:
                    logging.error(f'Problem with storing ticker in Redis: {e}')
                    continue
            else:
                company = json.loads(x)               
            measures_data = {}


            # print('COMPANY',company)
            all.append(json.dumps(company))
            print(all,'ALL COMPANIES FETCHED',len(all))
            if (company['ebitdaMargins'] <= (discount + perc) and company['ebitdaMargins'] >= (perc-discount)):
                for measure in valuation_measures:
                    try:
                        value = company[measure]
                        measures_data[measure] = value
                    except KeyError:
                        logging.error('key error')
                        measures_data[measure] = None
                valuation_data[ticker] = measures_data
                print('Dtype:',isinstance(measures_data['trailingPE'],float))
                if isinstance(measures_data['trailingPE'],float) and isinstance(measures_data['enterpriseToRevenue'],float) and isinstance(measures_data['enterpriseToEbitda'],float) :
                    # st.write(measures_data['trailingPE'])
                    if measures_data['trailingPE'] <40 or measures_data['enterpriseToEbitda'] < 25 or measures_data['enterpriseToRevenue'] < 6 :
                        total_ev_ebidta += measures_data['enterpriseToEbitda']
                        total_ent_rev += measures_data['enterpriseToRevenue']       
                        total_p_e += measures_data['trailingPE']
                        medev.append(measures_data['enterpriseToEbitda'])
                        medrev.append(measures_data['enterpriseToRevenue'])
                        medpe.append(measures_data['trailingPE'])
                        tot = tot + 1

        except:
            logging.error(f'No valid ticker for this.')
            continue

        try:
            avg_ev_ebidta = (total_ev_ebidta / tot) * (1-discount)
            avg_ent_rev = (total_ent_rev / tot) * (1-discount)
            avg_p_e = (total_p_e / tot) * (1-discount)


            median_ev_ebidta = statistics.median(medev)* (1-discount)
            median_ent_rev = statistics.median(medrev)* (1-discount)
            median_p_e = statistics.median(medpe)* (1-discount)
            avg1.append(avg_ev_ebidta)
            med1.append(median_ev_ebidta)
            avg2.append(avg_ent_rev)
            med2.append(median_ent_rev)
            avg3.append(avg_p_e)
            med3.append(median_p_e)       
        except Exception as e:
            logging.error(f'No valid tickers to calculate averages. {e}')
            return jsonify({'error': str(e)}), 400



def parse_types(cell):
   try:
       json_data = json.loads(cell) 
       types_list = json_data.get('type', '').split(', ')
       return types_list
   except (json.JSONDecodeError, AttributeError):
       return []


def filter_by_types(df , types_list):
   filtered_df = df[df['Types'].apply(lambda x: any(t in x for t in types_list))]
   return filtered_df


def valuations():
    try:
        data = request.get_json()
        ebitda = data.get('ebitda', '')
        revenue = data.get('revenue', '')
        net_income =data.get('net_income', '')
        debt = data.get('debt', '')
        cash = data.get('cash', '')
        selected_country = data.get('selected_country','')
        types_to_filter = data.get('types_to_filter',[])
        industry = data.get('sector','')

        logging.info('Valuations data from frontend',data)

        if industry == "Food & Beverages":
            file_path = 'fin_stock.xlsx'
            try:
                df = pd.read_excel(file_path)
                df = df.drop_duplicates(subset=['Symbol','Name','Country','longBusinessSummary','Subsector'], keep='first')
                df = df.dropna(subset=['Subsector'])
                # df['Types'] = df['Subsector'].apply(parse_types)
                # df = filter_by_types(df,types_to_filter)

            except:
                logging.error('Excel file error in loading')

        else:
            file_path =  'ticker_info.xlsx'
            try:
                df = pd.read_excel(file_path)
                df = df.drop_duplicates(subset=['Symbol','Country'], keep='first')
                df = df.dropna(subset=['Country'])
                # df['Types'] = df['Subsector'].apply(parse_types)
                # df = filter_by_types(df,types_to_filter)


            except:
                logging.error('Excel file error in loading')

        

        unique_countries = df['Country'].unique()
        not_selected = []


        if selected_country in gr_1['countries']:
            discount = gr_1['discount']
            selected_group = gr_1
            disc1 = 0.25
            disc2 = 0.30
            not_selected = [gr_2,gr_3]
        elif selected_country in gr_2['countries']:
            discount = gr_2['discount']
            selected_group = gr_2
            disc1 = 0.20
            disc2 = 0.30
            not_selected = [gr_1,gr_3]


        elif selected_country in gr_3['countries']:
            discount = gr_3['discount']
            selected_group = gr_3
            disc1 = 0.25
            disc2 = 0.20
            not_selected = [gr_2,gr_1]


        filtered_df = df[df['Country'].isin(selected_group['countries'])]

        if industry == "Food & Beverages":
            print('here')
            filtered_df = df[df['Subsector'].isin(selected_group['countries'])]


        # Get the list of symbols for the selected group
        symbols_list = filtered_df['Symbol'].tolist()
        # print(filtered_df)
        symbols_unselected_dict = {}
        for i, group in enumerate(not_selected, 1):
            symbols_list_unselected = df[df['Country'].isin(group['countries'])]['Symbol'].tolist()
            symbols_unselected_dict[f"Symbols for unselected group {i}"] = {'symbols': symbols_list_unselected, 'discount': group['discount']}


        # print(symbols_unselected_dict)
        perc = ebitda/revenue
        group_wise_calculations(symbols_list=symbols_list,perc=perc,discount=discount)
        group_wise_calculations(symbols_list=symbols_unselected_dict['Symbols for unselected group 1']['symbols'],discount=disc1,perc=perc)
        group_wise_calculations(symbols_list=symbols_unselected_dict['Symbols for unselected group 2']['symbols'],discount=disc2,perc=perc)
        ev_avg =  average(avg1)
        ev_rev = average(avg2)
        ev_pe = average(avg3)
        ev_med =  statistics.median(med1)
        evrev_med = statistics.median(med2)
        ev_pe_med = statistics.median(med3)
        net_debt = debt - cash
        print(ev_avg,ev_med,ev_rev,ev_med,ev_pe,ev_pe_med)
        ltme =  [(ev_avg * ebitda) - net_debt, ev_med * ebitda]
        ltmqe = [(ev_rev * revenue) - net_debt, evrev_med * revenue]
        ltmpe = [ev_pe * net_income, ev_pe_med * net_income]
        data = {
            "ltme": ltme,
            "ltmqe": ltmqe,
            "ltmpe": ltmpe
        }


        fin = json.dumps(data)
        logging.info('Final Valuation result',fin)
        return fin
    except Exception as e:
        logging.error(f'Valuation failed {e}')
        return jsonify({'error': str(e)}), 500

def companyList():
    company_list = []
    try:
        file_path = 'stock_info.xlsx'
        try:
            df = pd.read_excel(file_path)
            df = df.drop_duplicates(subset=['Symbol','Name','Country'], keep='first')
        except Exception as e:
            logging.error(f'Excel file error in loading: {e}')
            return jsonify({'error': str(e)}), 500
      
        symbols_list = df['Symbol'].tolist()
        selected_symbols = random.sample(symbols_list, 20)
        for ticker in selected_symbols:
            try:
                company = yf.Ticker(ticker)
                print(company)
                logging.info(f'Fetched ticker {ticker} successfully')
            except Exception as e:
                logging.error(f'Failed to fetch ticker {ticker}: {e}')
                continue
                
            try:
                info_dict = company.info
                if isinstance(info_dict, dict):
                    set_redis_key(ticker, json.dumps(info_dict), ttl=86400)
                    logging.info(f'Ticker {ticker} stored in Redis')
                else:
                    logging.error(f'Company info for ticker {ticker} is not a dictionary')
                    continue
            except Exception as e:
                logging.error(f'Problem with storing ticker {ticker} in Redis: {e}')
                continue
                
            keys_to_extract = ['symbol', 'priceHint', 'regularMarketDayHigh', 'regularMarketDayLow', 'exchange', 'volume']
            result_dict = {key: info_dict[key] for key in keys_to_extract if key in info_dict}
            company_list.append(result_dict)
        
        data = {"companies": company_list}
        logging.info('Companies data: %s', json.dumps(data))
        return json.dumps(data)

    except Exception as e:
        logging.error(f'Valuation failed: {e}')
        return jsonify({'error': str(e)}), 500
