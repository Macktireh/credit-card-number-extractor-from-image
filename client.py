import httpx
import asyncio


url_v1 = "http://127.0.0.1:8000/api/v1/extract-card-number"
url_v2 = "http://127.0.0.1:8000/api/v2/extract-card-number"

async def main() -> None:
    async with httpx.AsyncClient() as client:
        files = {'image': open('./static/card/all_2000.jpg', 'rb')}
        response = await client.post(url_v1, files=files)
        body = response.json()
        if response.status_code == 200:
            card_number = body.get('cardNumbers')
            print(len(card_number))
            print(card_number)
        else:
            print("Error:", body.get('detail').get('message'))


if __name__ == "__main__":
    asyncio.run(main())
