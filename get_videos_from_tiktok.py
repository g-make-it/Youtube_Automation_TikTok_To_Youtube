from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import os
import requests
import uuid
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
class FetchVideos():

    def value_to_float(self,x):
        if type(x) == float or type(x) == int:
            return x
        if 'K' in x:
            if len(x) > 1:
                return float(x.replace('K', '')) * 1000
            return 1000.0
        if 'M' in x:
            if len(x) > 1:
                return float(x.replace('M', '')) * 1000000
            return 1000000.0
        if 'B' in x:
            return float(x.replace('B', '')) * 1000000000
        return 0.0

    def try_to_get_video(self,link, search_term):
        try:
            video_data = requests.get(link)
            path = './videos/'
            total_path = path + search_term
            if not os.path.exists(total_path):
                os.makedirs(total_path)
            open(total_path+f'/{str(uuid.uuid4())}.mp4', 'wb').write(video_data.content)
            print('file written')
        except Exception as e:
            print(e, 'unable to get video')

    def run(self, target_string):

        list_of_video_links = []
        driver = webdriver.Chrome( executable_path=ChromeDriverManager().install())
        # driver.get("https://www.tiktok.com/")

        search_term = target_string
        # search_term = "Can't You See Me?"
        chars = "\\`*_{}[]()>#+-.!$?�"
        for c in chars:
            search_term = search_term.replace(c,'')

        path = './videos/'
        total_path = path+search_term
        if not os.path.exists(total_path):
            os.makedirs(total_path)
        driver.get(f"https://www.tiktok.com/tag/{search_term}")


        '''
        Waiting for page of all content to show up
        '''

        for i in range(20):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
            except Exception as e:
                print(e, 'could not press search for new content')


        html = driver.page_source
        html = BeautifulSoup(html, 'html.parser')

        all_a_values = html.findAll('a')
        list_of_hrefs = []
        for value in all_a_values:
            temp = value['href']
            if 'https://www.tiktok.com/@' == temp[:24]:
                list_of_hrefs.append(temp)


        for link in list_of_hrefs:
            # try using requests here
            driver.get(link)
            try:
                element_of_likes = driver.find_elements(By.XPATH, '//*[@data-e2e="like-count"]')[0]
                number_of_likes = self.value_to_float(element_of_likes.text)
                if number_of_likes > 10000:
                    element_video = driver.find_element(By.XPATH, '//video[@src]')
                    video_url = element_video.get_attribute('src')
                    if video_url in list_of_video_links:
                        continue

                    if len(list_of_video_links) > 200:
                        break
                    list_of_video_links.append(video_url)
            except Exception as e:
                print('issue in finding the video link')

        for item in list_of_video_links:
            self.try_to_get_video(link=item, search_term=search_term)

        driver.quit()
        print('gathering video completed')
# testing
if __name__ == '__main__':
    fv = FetchVideos()
    target_string = "Dance"
    fv.run(target_string)