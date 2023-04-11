# The task is parsed from the website https://www.coingecko.com
# Cryptocurrency prices on exchanges from the list of exchanges
# The number of pages and with some pages the parse is adjusted below the corresponding numbers
# The percentage difference in the value of cryptocurrency on exchanges in ET_VIDSOTOK
# Total The output csv file includes only those cryptocurrencies that will be found on exchanges
# difference in prices corresponding to the set percentage.
# Result on disk C:\coingeckoXX-XX.csv Published in files on page PAGEG.
# You can buy on one exchange and sell cryptocurrency on another exchange and earn money!


from bs4 import BeautifulSoup
import requests

ET_VIDSOTOK = 4 # Percentage difference between price
PAGEG = 2 # How many pages to put in a file
page = 5 # From which page we start parsing

# List of exchanges to check
exchanges = ['digifinex', 'binance', 'aex', 'gate-io', 'mexcglobal', 'bkex', 'huobi', 'bitforex', 'hotbit', 'whitebit', 'bybit_spot']

# Currency exceptions
valuta = ['UAH', 'RUB']

#count_page = int(soup[0]) # We parse all pages from the site
count_page = 2 # We parse this number of pages from the site

header = {"Accept": "text/html, application/xhtml+xml, image/jxr, */*", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0", "Accept-Language": "en-US;q=0.7", "Accept-Encoding": "deflate", "Cache-Control": "no-cache", "Connection": "keep-alive"}
r = requests.get('https://www.coingecko.com/uk', headers=header, verify=False)
soup = r.text.split('class="page-link">')
soup = soup[7].split('<')
page_tek = page

for p in range(count_page):
    if p + page == page_tek:
        try:
            f.close()
        except Exception:
            pass
        page_tek = p + page + PAGEG
        f = open('D:\coingecko' + str(p+page) + '-' + str(page_tek - 1) + '.csv', 'w')
        f.write('Монета;Пара;Биржа;Цена;Проценты;Разница\n')
    r = requests.get('https://www.coingecko.com/uk?page=' + str(p+page), headers=header, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
#    print(page+p)
    items = soup.find_all('a', class_='tw-flex tw-flex-auto tw-items-start md:tw-flex-row tw-flex-col')
    i = 0
    for i in range(len(items)):
        url = items[i].attrs['href']
        print(str(page+p) + ' ', items[i].text.replace('\n', '').strip())
        r2 = requests.get('https://www.coingecko.com' + url, headers=header, verify=False)
        s_tmp = r2.text.split('<input type="hidden" name="coin_id" id="coin_id" value="')
        s_tmp = s_tmp[1].split('"')
        r2 = requests.get('https://www.coingecko.com/uk/coins/'+s_tmp[0]+'/markets_tab', headers=header, verify=False)
        soup2 = BeautifulSoup(r2.content, 'html.parser')
        items2 = soup2.find_all('tr', class_='')
        lines = []
        n = -1
        m = -1
        j = 0
        for j in range(len(items2)-1):
            try:
                para = items2[j+1].contents[5].text.replace('\n', '')
                href_para = items2[j+1].contents[5].contents[1].attrs['href']
                price = items2[j+1].contents[7].contents[1].attrs['data-price-btc']
                percent = items2[j+1].contents[17].text.replace('\n', '')
                n = -1
                ex = 0
                for ex in range(len(exchanges)):
                    n = href_para.find(exchanges[ex])
                    if n > -1:
                        break
                if float(percent.replace('%', '').replace(',', '.')) > 0 and n > -1:
                    lines.append([0] * 5)
                    m = m + 1
                    lines[m][0] = para
                    lines[m][1] = href_para
                    lines[m][2] = float(price)
                    lines[m][3] = price
                    lines[m][4] = float(percent.replace('%', '').replace(',', '.'))
            except Exception:
                pass
        lines = sorted(lines, key=lambda x: x[2], reverse=True)
        k = 0
        max_vidsotok = 1
        if m > 1:
            est_vidsotok = False
            try:
                for k in range(len(lines)):
                    if lines[k][0] != 0 and (lines[k][0]).find('реального') == -1:
                        va = 0
                        for va in range(len(valuta)):
                            if lines[k][0].find(valuta[va]) != -1:
                                raise StopIteration
                        if k == 0:
                            max_vidsotok = lines[k][2]
                        else:
                            vidsotok = str(100 - int(lines[k][2] * 100 / max_vidsotok))
                            if int(vidsotok) >= ET_VIDSOTOK:
                                est_vidsotok = True
                                break
            except StopIteration:
                est_vidsotok = False
            if est_vidsotok == True:
                f.write(items[i].text.replace('\n', '') + ';;;;;\n')
                k = 0
                vidsotok = ''
                for k in range(len(lines)):
                    if lines[k][0] != 0 and (lines[k][0]).find('реального') == -1:
                        if k == 0:
                            max_vidsotok = lines[k][2]
                        else:
                            vidsotok = str(100 - int(lines[k][2] * 100 / max_vidsotok))
                            if int(vidsotok) < ET_VIDSOTOK:
                                vidsotok = ''
                        f.write(';'+str(lines[k][0]) + ';' + str(lines[k][1]) + ';' + str(lines[k][3]) + ';' + str(lines[k][4]) + ';' + vidsotok+'\n')
f.close()