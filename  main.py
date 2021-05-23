import configparser
import requests
import json
import winsound
from pycoingecko import CoinGeckoAPI
from setInterval import set_interval


config = configparser.ConfigParser()
config.read('config.ini')

BASE_URL = 'https://api2.nicehash.com/main/api/v2/public'
BTC_TO_USD = 0

def getDevices():
    request = requests.get('{}/profcalc/devices'.format(BASE_URL))
    body = request.json()
    gpus = [{ 'name': device['name'], 'id': device['id'] } for device in body['devices'] if device['category'] == 'GPU']
    return gpus

def getSpeeds(cardId):
    request = requests.get('{}/profcalc/device?device={}'.format(BASE_URL, cardId))
    body = request.json()
    return body['speeds']


def getProfitabilityForCard(speeds):
    requestBody = {
        'speeds': speeds,
    }
    request = requests.post('{}/profcalc/profitability'.format(BASE_URL), data=json.dumps(requestBody), headers={ 'Content-Type': 'application/json;charset=UTF-8' })
    body = request.json()
    values = [float(btcValue['p']) for btcValue in body['values'].values()]
    return sum(values) / len(values)

def getBTCPrice():
    cg = CoinGeckoAPI()
    return cg.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']

def alert():
    print('Mining is profitable!')
    if config['Default']['displaySound'] == 'True':
        winsound.PlaySound('soundAlert.wav', winsound.SND_FILENAME)

def main():
    gpus = getDevices()
    selectedGpu = config['Default']['graphicsCard']
    if selectedGpu not in [ gpu['name'] for gpu in gpus ]:
        print('Invalid graphics card!')
    gpu = next(gpu for gpu in gpus if gpu['name'] == selectedGpu)
    print('Checking gpu {}'.format(gpu['name']))
    speeds = json.loads(getSpeeds(gpu['id']))
    profitabilty = getProfitabilityForCard(speeds)

    if ('minBtcPerDay' not in config['Default'] and 'minUsdPerDay' not in config['Default']) or 'minBtcPerDay' in config['Default'] and 'minUsdPerDay' in config['Default']:
        print('Invalid config. No minimum set, you should set either minBtcPerDay or minUsdPerDay')

    if 'minBtcPerDay' in config['Default']:
        if profitabilty > float(config['Default']['minBtcPerDay']):
            alert()
    else:
        priceInUsd = profitabilty * getBTCPrice()
        if priceInUsd >= float(config['Default']['minUsdPerDay']):
            alert()
        else:
            print('Profitability is below threshold, expected {} and got {}'.format(float(config['Default']['minUsdPerDay']), priceInUsd))

set_interval(main, int(config['Default']['timeInterval']))