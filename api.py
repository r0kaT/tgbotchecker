import asyncio
import requests

def get_allocation_sync(address: str, platform: str) -> str:
    if platform == "jup":
        url = "https://jupuary.jup.ag/api/allocation"
        params = {"wallet": address}
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'referer': f'https://jupuary.jup.ag/allocation/{address}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/134.0.0.0 Safari/537.36',
        }
    elif platform == "kiloex":
        url = "https://mantaapi.kiloex.io/point/queryKiloAccountAward"
        params = {"account": address}
        headers = {
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://app.kiloex.io/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/134.0.0.0 Safari/537.36',
        }
    elif platform == "hyperlane":
        url = "https://claim.hyperlane.foundation/api/check-eligibility"
        params = {"address": address}
        headers = {
            'accept': '*/*',
            'referer': 'https://claim.hyperlane.foundation/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            
        }
    else:
        return f"{address} ➡ Unknown platform ❌\n"

    try:
        response = requests.get(url, params=params, headers=headers)
        response_data = response.json()
        if platform == "jup":
            data = response_data.get("data")
            if data is None:
                return f"❌{address} ➡ You are not a participant of Jup "
            allocation = data.get("total_allocated", 0)
            return f"✅ {address} ➡ {allocation}" if allocation > 0 else f"❌{address} ➡ Not Eligible"
        elif platform == "kiloex":
            allocation = response_data["data"]["kilo"]
            return f"{address} ➡ {allocation}"
        elif platform == "hyperlane":
            data = response_data["response"]["isEligible"]
            if data == False:
                return f"❌{address} ➡ Not Eligible"
            allocation = response_data["response"]["eligibilities"][0]["amount"]
            return f"✅{address} ➡ {allocation} "
    except requests.exceptions.RequestException as e:
        return f"{address} Ошибка сети: {e} ❌"

async def get_allocation(address: str, platform: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_allocation_sync, address, platform)