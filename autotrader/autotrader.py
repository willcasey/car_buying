import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Autotrader:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.page_num = None
        self.xpath_dict = self.XPathDict()
        self.data_columns = ['name', 'price', 'mileage', 'miles_away', 'phone_number', 'dealership_name']
        self.df = pd.DataFrame(columns=self.data_columns, index=[])
                        
                                
        
    def getDriver(self, page_num):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())  
        self.driver.get(self.url.format(page_num = page_num*25))  
    
    def getIds(self):
        ids_list = []
        ids = self.driver.find_elements_by_xpath('//*[@id]')
        for ii in ids:
            if ii.tag_name == 'div' and len(re.findall(r'\d{9}',ii.get_attribute('id'))) > 0:
                try:
                    ids_list.append(int(ii.get_attribute('id')))
                except:
                    None
        return ids_list
    
    def XPathDict(self):
        xpathdict = { 'name': '//*[@id="{i_d}"]/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[1]/div/a/h2'
                    , 'price': '//*[@id="{i_d}"]/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div[2]'
                    , 'mileage': '//*[@id="{i_d}"]/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[2]/span'
                    , 'miles_away': '//*[@id="{i_d}"]/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/span'
                    , 'phone_number': '//*[@id="{i_d}"]/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/span'
                    , 'dealer_name': '//*[@id="{i_d}"]/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]'
                    }
        return xpathdict
    

    
    
    def getXPathData(self, xpath, i_d):
        try:
            return self.driver.find_element_by_xpath(xpath.format(i_d=i_d)).text
        except:
            return None
        
    
    def getAllData(self):
        for i_d in self.getIds():
            data = []
            for xpath in self.xpath_dict:
                data.append(self.getXPathData(xpath=self.xpath_dict[xpath], i_d=i_d))
                
            if any(data): #checks to see if the list data has all 'None' values
                self.df = self.df.append(pd.Series(data, index=self.data_columns), ignore_index=True)
                
                
                
    def getAllPagesData(self, max_page, delay=20):
        for page_num in range(max_page):
            self.getDriver(page_num = page_num)
            self.getAllData()
            WebDriverWait(self.driver, delay)
            self.driver.close()
            
