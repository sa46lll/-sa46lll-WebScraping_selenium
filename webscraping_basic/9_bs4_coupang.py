import requests
import re
from bs4 import BeautifulSoup

url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=1&rocketAll=false&searchIndexingToken=1=4&backgroundColor="
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

# print(res.text)
items = soup.find_all("li", attrs={"class" : re.compile("^search-product")}) # search_product 로 시작하는 모든 "li" element
# print(items[0].find("div", attrs={"class" : "name"}).get_text())

for item in items:

    # 광고 제품은 제외
    ad_badge = item.find("span", attrs={"class" : "ad-badge-text"})
    if ad_badge:
        print(" <광고 상품 제외합니다>  ")
        continue

    name = item.find("div", attrs={"class" : "name"}).get_text() # 제품명
    # 애플 제품 제외
    if "Apple" in name:
        print(" <Apple 상품 제외합니다.> ")
        continue
    
    price = item.find("strong", attrs={"class" : "price-value"}).get_text() # 가격

 
    # 리뷰 100개 이상, 평점 4.5 이상 되는 것만 조회
    rating = item.find("em", attrs={"class" : "rating"}) # 평점
    if rating:
        rating = rating.get_text()
    else :
        print(" <평점 없는 상품 제외합니다> ")
        continue

    rating_cnt = item.find("span", attrs={"class" : "rating-total-count"}) # 평점 수
    if rating_cnt:
        rating_cnt = rating_cnt.get_text()
        rating_cnt = rating_cnt[1:-1]
        # print("리뷰 수 : " + rating_cnt)
    else : 
        print(" <평점 수 없는 상품 제외합니다> ")
        continue

    if float(rating) >= 4.5 and int(rating_cnt) >= 100:
        print(name, price, rating, rating_cnt)
