import asyncio
from cotação import main as cot

async def fii():
    cotação = cot()
    print("Exce")
    await cotação.programa("fii")

async def bdr():
    cotação = cot()
    print("executado")
    await cotação.programa("bdr")
    

async def main():
    await asyncio.gather(bdr(), fii())


asyncio.run(main())