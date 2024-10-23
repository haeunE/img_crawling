from selenium import webdriver
import os
from urllib.request import urlopen
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def Driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #options.add_argument("headless")
    options.add_argument('--start-fullscreen')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome(options = options)
    return wd

# 베이스 URL과 상업적 이용 가능 옵션
def make_url(word):
    base_url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=image&query='
    ccl = '&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=2&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&recent=0&datetype=0&startdate=0&enddate=0&gif=0&optStr=&nso_open=1&pq='
    return base_url + word + ' 캔' + ccl

# 해당하는 폴더가 없을 경우 생성해주는 함수
def makedirs(path): 
   try: 
        os.makedirs(path) 
   except OSError: 
       if not os.path.isdir(path): 
           raise

# 찾을 목록이 담긴 dictionary
# search_dict = {
#         '과즙음료' : ['갈아만든배','쌕쌕','코코팜','비락식혜','비락수정과', '봉봉'],
#         '커피' : ['조지아','레쓰비','산타페','티오피','칸타타'],
#         '카페인음료' : ['박카스','핫식스','레드불','몬스터에너지'],
#         '이온음료' : ['게토레이','포카리스웨트','토레타','파워에이드'],
#         '탄산음료' : ['코카콜라','칠성사이다','웰치스_포도','환타','마운틴듀'],
#         '기타' : ['데자와','실론티','초코에몽','제티']
#         }
search_dict = {
        '기타' : ['데자와','실론티','초코에몽','제티']
        }

def save_images(image_url, paths, file_name, i):
    import base64
        
    if 'data:' in str(image_url):
        pass
    else:
        t= urlopen(image_url).read()
        file = open(os.path.join(paths, file_name+'_'+str(i)+".gif"), 'wb')
        file.write(t)

def naver_crawl(image_numbers):
    wd = Driver()
    wd.implicitly_wait(3)
    for meal in search_dict:
        #종류 별 파일 생성
        file_path = os.getcwd()+f'\{meal}'
        makedirs(file_path)
        for food in search_dict[meal]:
                # 음식에 해당하는 검색어를 입력한 페이지 출력
                print(f"------------------ Start {meal} / {food} ----------------------")
                wd.get(make_url(food))
                time.sleep(2)
                for i in range(1,image_numbers+1):
                    time.sleep(2)
                    # i에 해당하는 이미지가 없을 경우 PASS
                    save_path= file_path + f'\{food}'
                    makedirs(save_path)
                    try:
                        # image url 추출
                        images= wd.find_elements(By.XPATH, f'//*[@id="main_pack"]/section/div[1]/div/div/div[1]/div[{i}]/div/div/div/img')
                        
                        print(save_path)

                        src = images[0].get_attribute('src')
                        save_images(str(src), save_path, f'{meal}_{food}_', i)
                        
                        # 이미지가 10개가 넘어갈때 마다 PAGE_DOWN
                        if i % 10 == 0:
                            body = wd.find_element(By.XPATH,'//body').send_keys(Keys.PAGE_DOWN)
                            time.sleep(3)
                    except:
                        print(f"No element in {i}")
                        continue
                print(f"------------------ end {meal} / {food} ----------------------")
    wd.close()
    print("End_crawling")
naver_crawl(50)