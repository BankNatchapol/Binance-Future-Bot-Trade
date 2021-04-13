import logging
import requests

logger = logging.getLogger()

def get_contracts():
    response = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")

    contracts = []

    for contract in response.json()['symbols']:
        contracts.append(contract['pair'])

    return contracts