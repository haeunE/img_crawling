from selenium import webdriver
import os
from urllib.request import urlopen
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib

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
    base_url = 'https://www.google.com/search?sca_esv=8a44ed1edae166f5&q='
    ccl = '&udm=2&fbs=AEQNm0DmKhoYsBCHazhZSCWuALW8mC6u5PFP1Ks3xvlaC0GwVFDphqJATVlK4Xe8ceC4SiPQ-LNnsfuQkOZlPe8yEeHmV4PvRpWxW6xOeSRTxNdclVwuBiRauG_UEqdcJjneBP9mw_9pGfxLUdd5tiSxaH7SArUJ0Pra47k6FEN1Xokj6EnaBkbEFKMeC8UN7gyIFg--SOwl&sa=X&ved=2ahUKEwiJ2Lqzx6OJAxUZk1YBHdlMNi8QtKgLegQIEBAB&biw=929&bih=873'
    return base_url + word + '+캔' + ccl

# 해당하는 폴더가 없을 경우 생성해주는 함수
def makedirs(path): 
  try: 
    os.makedirs(path) 
  except OSError: 
    if not os.path.isdir(path): 
      raise

# 찾을 목록이 담긴 dictionary
search_dict = {
        '과즙음료' : ['갈아만든배','쌕쌕','코코팜','비락식혜','비락수정과', '봉봉'],
        '커피' : ['조지아','레쓰비','산타페','티오피','칸타타'],
        '카페인음료' : ['박카스','핫식스','레드불','몬스터에너지'],
        '이온음료' : ['게토레이','포카리스웨트','토레타','파워에이드'],
        '탄산음료' : ['코카콜라','칠성사이다','웰치스_포도','환타','마운틴듀'],
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

def google_crawl():
    driver = Driver()
    driver.implicitly_wait(3)
    for meal in search_dict:
        #종류 별 파일 생성
        file_path = os.getcwd()+f'\{meal}'
        makedirs(file_path)

        for food in search_dict[meal]:
            # 음료에 해당하는 검색어를 입력한 페이지 출력
            print(f"------------------ Start {meal} / {food} ----------------------")
            driver.get(make_url(food))
            time.sleep(2)
            
            # 페이지 스크롤 
            elem = driver.find_element(By.TAG_NAME,'body')
            for i in range(1): #스크롤 횟수 지정
              elem.send_keys(Keys.PAGE_DOWN)
              time.sleep(1) # 쉬어주기
            try:
                button = driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
                button.click() # 스크롤을 내리다보면 '결과 더보기'가 있는 경우 버튼 클릭
                time.sleep(1)
            except:
                pass
            # if driver.find_element(By.CLASS_NAME, 'OuJzKb.Yu2Dnd').text == '더 이상 표시할 콘텐츠가 없습니다.': # class 이름으로 가져오기
            #     break
            
            # 음료 별 파일 생성 
            save_path= file_path + f'\{food}'
            makedirs(save_path) 


            # 이미지 수집 및 저장
            images = driver.find_elements(By.CLASS_NAME, "mNsIhb") # 각 이미지들의 class
            count = 1
            for image in images:
                try:
                    image.click()
                    time.sleep(1)
                    imgUrl = driver.find_element(By.XPATH,
                        '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[3]/div[1]/a/img').get_attribute("src")
                    
                    save_images(imgUrl, save_path, f'{meal}_{food}_', count)
                    # urllib.request.urlretrieve(imgUrl, f'train_dataset/{searchKey}/{searchKey}_{str(count)}.jpg') # url을 
                    count = count + 1
                    print(f'--{food} {count}번째 이미지 저장 완료--')
                except Exception as e:
                    print(f"No element in {count}")
                    # print('Error : ', e)
            print(f"------------------ end {meal} / {food} ----------------------")
    driver.close()
    print("End_crawling")

google_crawl()
