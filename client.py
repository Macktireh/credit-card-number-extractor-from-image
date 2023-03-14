import httpx
import asyncio


url = "http://localhost:8000/extract-card-number"

async def main() -> None:
    async with httpx.AsyncClient() as client:
        files = {'image': open('./static/card/all_500.jpg', 'rb')}
        response = await client.post(url, files=files)
        body = response.json()
        if response.status_code == 200:
            card_number = body.get('cardNumbers')
            print(len(card_number))
            print(card_number)
        else:
            print("Error:", body.get('detail').get('message'))


if __name__ == "__main__":
    asyncio.run(main())
