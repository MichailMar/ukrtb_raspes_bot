from aiohttp import client
import asyncio
from bs4 import BeautifulSoup 
from bs4 import PageElement
from  .exception import ItemError, NotTimeTable

class StudyPars:
    
    def __init__(self, item: str, date: str, type: str) -> None:
        self.item = item
        self.date = date
        self.type = type

    async def _get_item(self) -> str:
        async with client.ClientSession() as session:
            async with session.get("https://study.ukrtb.ru/timetable") as resp:
                markup = await resp.text()        

        soup = BeautifulSoup(
            markup = markup, 
            features = "lxml"
            )
        
        item = soup.find("option", string=self.item)
        if item == None:
            raise ItemError(self.item)
        return item.attrs['value']

    async def _get_timetable(self) -> dict[str, list[dict[str, str]]]:
        item: str = await self._get_item()
        
        async with client.ClientSession() as session:
            async with session.get(f"https://study.ukrtb.ru/timetable/get?type={self.type}&item={item}&inputDate={self.date}") as resp:
                timetable = await resp.text()

        soup = BeautifulSoup(
            markup = timetable,
            features = "lxml"
            )
        
        lists: list = []

        i: PageElement

        if soup.find("p").get_text() == "Расписание отсутствует":
            raise NotTimeTable(self.item, self.date)
        
        for i in soup.find_all("div", attrs={"class": "row"}):
            child =  i.findChildren("h4")
            if len(child) == 0:
                continue
            lists.append({"time": child[0].get_text(), "name": child[1].get_text(), "cab": child[2].get_text()})
        
        return {soup.find("h3").get_text().replace("\n", "").replace(" ", ""): lists}
    
    async def get_timetable(self) -> dict[str, list[dict[str, str]]]:
        return await self._get_timetable()

    async def get_all_item(self) ->  dict[str, str]:
        async with client.ClientSession() as session:
            async with session.get("https://study.ukrtb.ru/timetable") as resp:
                markup = await resp.text()        

        soup = BeautifulSoup(
            markup = markup, 
            features = "lxml"
            )
        
        items = soup.find("select", attrs={"id": f"{self.type}Select"})
        
        res = {}
        i: PageElement

        for i in items.findChildren("option"):
            if not "value" in i.attrs:
                continue
            res.update({i.get_text(): i.attrs['value']})

        return res

if __name__ == "__main__":
    p = StudyPars("Бокуменко Алекс Витальевич", "2022-12-13", "teacher")
    #teacher - училки group - группы cab - кабинеты
    loop = asyncio.new_event_loop() # if you version < python3.10 use asyncio.get_event_loop
    print(loop.run_until_complete(p.get_all_item()))