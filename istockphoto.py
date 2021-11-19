import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import time
import math
import random


def main():
    start_time = time.time()

    cur_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())

    ua = UserAgent()
    user_agent = ua.random
    headers = {
        'User-Agent': user_agent
    }

    keyword = input("請輸入要搜尋的食物: ")
    if " " in keyword:
        keyword = keyword.replace(" ", "%20")

    if not os.path.exists('./{}_{}'.format(keyword.replace("%20", " "), cur_time)):
        os.mkdir('./{}_{}'.format(keyword.replace("%20", " "), cur_time))

    pages = int(input("請輸入要搜尋的頁數(可以先進網頁看看他有幾頁XD): "))

    url = "https://www.istockphoto.com/search/2/image?mediatype=&phrase=%20{}&mediatype=&page=1".format(keyword)

    ss = requests.session()

    for i in range(1, pages + 1):
        res = ss.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        # print(soup)
        photos = soup.select('img[class="MosaicAsset-module__thumb___tdc6z"]')
        for index, photo in enumerate(photos):
            time.sleep(random.randint(3, 10)/10)
            food_pic_link = photo['src']
            res_img = requests.get(food_pic_link)
            print(food_pic_link)
            print("---------------------------------")
            try:
                img_local_path = './{}_{}/{}_istockphoto_page{}_{}.jpg'.format(keyword.replace("%20", " "), cur_time,
                                                                        keyword.replace("%20", " "), i, str(index+1))
                with open(img_local_path, 'wb') as f:
                    f.write(res_img.content)
            except OSError as o:
                print(o)

        page = i + 1
        url = "https://www.istockphoto.com/search/2/image?mediatype=&phrase=%20{}&mediatype=&page={}".format(keyword,
                                                                                                             page)

    execute_time = time.time() - start_time
    print("共花 " + str(math.floor(execute_time)) + " 秒")


if __name__ == '__main__':
    main()
