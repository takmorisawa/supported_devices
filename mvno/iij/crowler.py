import os
dir=os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(os.path.dirname(os.path.dirname(dir)))

import time
from cleaning_shop.crowler import Driver, Crowler

class iijCrowler(Crowler):

    def scrape(self):
        print(0)
        items=self._d.xpath("//article[not(@style='display: none;')]")
        print("len: ", len(items))
        for item in items:
            xpath_list=[
                "//*[@id='fixidpoint']/div/label[contains(@class,'-select')]",
                ".//div[@class='dv-maker']",
                ".//div[@class='dv-name']",
                ".//div[@class='dv-size']",
                ".//div[@class='dv-tethe']/span[@class='-sp-center']",
                ".//div[@class='dv-voice']/span[@class='-sp-center']",
                ".//div[@class='dv-annotation']"
            ]
            print(1)
            row=[item.find_element_by_xpath(xpath).text for xpath in xpath_list]
            print(row[2])
            self.append(row)

    def crowl(self):
        self._d=Driver()
        #self._headless=True
        self._d.open("https://www.iijmio.jp/hdd/devices/")
        #self.scrape()
        button=self._d.xpath(".//label[@class='-btn _a']")[0]
        button.click()
        self.scrape()



crowler=iijCrowler(["plna","maker","name","sim","tethering","call","note"])
crowler._filepath=os.path.join(dir,"tmp/csv/devices_iij-scraped.csv")
crowler.exec();
