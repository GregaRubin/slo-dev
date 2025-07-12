from scrappers.base_scrapper import BaseScrapper
from bs4 import BeautifulSoup
from requests import request
from datetime import datetime, timedelta

class MojedeloScrapper(BaseScrapper):
    def __init__(self, name: str):
        super().__init__(name)
    
    # returns array of job names, dates, and links
    def fetch_page_base_info(self, page_num):
        url = f"https://www.mojedelo.com/prosta-delovna-mesta/racunalnistvo-programiranje/vse-regije?p={page_num}"
        res = request("GET", url)
        if res.status_code != 200:
            self.error(f"Failed to fetch page {page_num}: {res.status_code}")
            return None
        
        soup = BeautifulSoup(res.text, 'html.parser')

    def run(self):
        url = f"https://www.mojedelo.com/prosta-delovna-mesta/racunalnistvo-programiranje/vse-regije"
        res = request("GET", url)
        if res.status_code != 200:
            self.error(f"Failed to fetch the page: {res.status_code}")
            return
        soup = BeautifulSoup(res.text, 'html.parser')

        for job_ad in soup.select('a.job-ad'):
            box_groups = job_ad.select('.boxItemGroup')
            date_text = None

            for group in box_groups:
                icon = group.select_one('.box-details-icon')
                
                if icon and 'icon-calendar' in icon.get('class', []):
                    detail = group.select_one('.detail')
                    if detail:
                        date_text = detail.get_text(strip=True).lower()
                        break  # found it

            # Parse the date string
            date_obj = None
            if date_text == 'danes':
                date_obj = datetime.today().date()
            elif date_text == 'včeraj':
                date_obj = (datetime.today() - timedelta(days=1)).date()
            else:
                try:
                    date_obj = datetime.strptime(date_text, '%d. %m. %Y').date()
                except ValueError:
                    pass  # unrecognized format

            print(f"Parsed date: {date_obj if date_obj else 'Unrecognized or missing'}")
