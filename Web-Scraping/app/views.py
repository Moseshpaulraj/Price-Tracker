from django.shortcuts import render
import requests
from datetime import date
from time import sleep
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
from time import sleep
from .models import *
from urllib.parse import urlparse, parse_qs
import urllib.parse
today = date.today()
todayDate=today.strftime("%d-%m-%Y")

from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent': ua.random}

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

context = {}

fname = []
fprice = []
fimage = []
foffer = []
furl = []
fid=[]

aname = []
aprice = []
aimage = []
aoffer = []
aurl = []
aid=[]

#---------------------------------------------------Telegram Notification--------------------------------------------#
async def notify(name, price, image, offer, url):
    image_data = requests.get(image).content
    bot = Bot(token="6269096560:AAGur6hchaokvs6QS2EmmZXNw9kbbjbQbo4")
    message = f'<b>{name}\nPrice: {price}\nOffer:{offer}</b>\n\n{url}'
    sleep(5)
    await bot.send_photo(chat_id=-1001846594182, photo=image_data,caption=message,parse_mode=ParseMode.HTML)


#-------------------------------------------------------------------------------------------------------------------#

def fidFinder(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    lid_value = query_params['lid'][0]
    return lid_value

# def aidFinder(url):
#     aid = urllib.parse.unquote(url)
#     aid=aid.split("dp/")[1]
#     aid=aid.split("/")[0]
#     return aid

#---------------------------------------------------Product Update-------------------------------------------------#
def fproduct_update(category,name,pid,price,offer,image,url):
    cate = Category.objects.get(name=category)
    for i in range(len(name)):

        if(FProducts.objects.filter(category=cate,fid=pid[i]).exists()):
            product = FProducts.objects.get(category=cate,fid=pid[i])

            if(product.price[-1] != price[i]):
                print("Price Changed",product.price[-1], price[i])
                print(url[i])
                print("----------------------------------------------------------------------------------------------")

                if(product.price[-1] < price[i]):
                    product.trending=False
                
                elif(product.price[-1] > price[i]):
                    product.trending=True
                    Notify.objects.create(name=name[i],image_link=image[i],url="https://price-tracker.up.railway.app/collections/"+str(category)+"/"+str(product.name).replace(" ","%20"),offer=offer[i],price=price[i])

                product.price.append(price[i])
                product.date.append(todayDate)

            if(product.offer!=offer[i]):
                product.offer=offer[i]

            if(product.image_link!=image[i]):
                product.image_link=image[i]

            if(product.url!=url[i]):
                product.url=url[i]
            
            product.save()

        else:
            product = FProducts.objects.create(category=cate,name=name[i],fid=pid[i],image_link=image[i],url=url[i],offer=offer[i],price=[price[i]],date=[todayDate])


def aproduct_update(category,name,pid,price,offer,image,url):
    cate = Category.objects.get(name=category)
    for i in range(len(name)):

        if(AProducts.objects.filter(category=cate,aid=pid[i]).exists()):

            product = AProducts.objects.get(category=cate,aid=pid[i])

            if(product.price[-1] != price[i]):
                print("Price Changed",product.price[-1], price[i])
                print(url[i])
                print("----------------------------------------------------------------------------------------------")

                if(product.price[-1] > price[i]):
                    product.trending=True
                    notify = Notify.objects.create(name=name[i],image_link=image[i],url="https://price-tracker.up.railway.app/collections/"+str(category)+"/"+str(product.name).replace(" ","%20"),offer=offer[i],price=price[i])
                
                elif(product.price[-1] < price[i]):
                    product.trending=False

                product.price.append(price[i])
                product.date.append(todayDate)


            if(product.offer!=offer[i]):
                product.offer=offer[i]

            if(product.image_link!=image[i]):
                product.image_link=image[i]


            if(product.url!=url[i]):
                product.url=url[i]
            

            product.save()

        else:
            product = AProducts.objects.create(category=cate,name=name[i],aid=pid[i],image_link=image[i],url=url[i],offer=offer[i],price=[price[i]],date=[todayDate])

#---------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------Details gathering-------------------------------------------------#
def amazon(url):
    while True:
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')


        main_class=soup.find("span",class_="rush-component s-latency-cf-section")

        if main_class is not None and main_class.find('div', class_='sg-col-20-of-24'):

            class1 = main_class.find_all('div',class_="sg-col-20-of-24")

            # class2=class1.find_all("div",class_="s-widget-container")
                
            # for class3 in class2:
                # all_products=class3.find_all("div",class_="s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t1 puis-include-content-margin puis s-latency-cf-section s-card-border")

            for all_product in class1:
                containers = all_product.find_all("div",class_="sg-row")

                for container in containers:

                    products = container.find_all('div', class_='sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right')
                    for product in products:
                        if(product.find('span', {'class': 'a-price-whole'}) and product.find_all("div",class_="a-row a-size-base a-color-base")):
                            
                            data_asin = all_product['data-asin']
                            if data_asin:
                                aid.append(data_asin)

                            names = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
                            # for name in names:
                            name = names.text
                            name=str(name).replace("/"," ").strip()
                            aname.append(name)

                            prices = product.find('span', {'class': 'a-price-whole'})
                            # for price in prices:
                            price = prices.text
                            price=str(price).replace(",","")
                            aprice.append(price)

                            offers = product.find("div",class_="a-row a-size-base a-color-base")
                            # for offers1 in offers:
                            offer=offers.find_all("span")[-2].text
                            offer=str(offer).replace("(","").replace(")","")
                            aoffer.append(offer)
                            break

                    for product in products:
                        if(product.find('span', {'class': 'a-price-whole'}) and product.find_all("div",class_="a-row a-size-base a-color-base")):
                            product_images = container.find_all("div",class_="sg-col sg-col-4-of-12 sg-col-4-of-16 sg-col-4-of-20 sg-col-4-of-24 s-list-col-left")
                            for product_image in product_images:
                                left=product_image.find("div",class_="s-product-image-container aok-relative s-text-center s-image-overlay-grey s-padding-left-small s-padding-right-small s-flex-expand-height")
                                images=left.find("img",class_="s-image")
                                # for image in images:
                                aimage.append(images.get("src"))
                                urls=left.find("a",class_="a-link-normal s-no-outline")
                                # for url in urls:
                                url = urls.get("href")
                                aurl.append("https://amazon.in"+str(url))
                                break
                        break

            next_url = soup.find('a',class_='s-pagination-next')
            if next_url is None:
                    break
            next=next_url.get("href")
            url="https://www.amazon.in"+str(next)
            print(url)

    print("--------------------------------------------------------------------------------------------------------------")
    print("Name",len(aname))
    print("Price",len(aprice))
    print("Offer",len(aoffer))
    print("Image",len(aimage))
    print("Url",len(aurl))
    print("Id",len(aid))
    print("--------------------------------------------------------------------------------------------------------------")


    lname=len(aname)
    if(lname==len(aprice) and lname==len(aoffer) and lname==len(aimage) and lname==len(aurl)):
        aproduct_update(category,aname,aid,aprice,aoffer,aimage,aurl)
    else:
        aname.clear()
        aprice.clear()
        aoffer.clear()
        aimage.clear()
        aurl.clear()
        aid.clear()

        a_url="https://www.amazon.in/s?k="+category+"&page=1&ref=sr_pg_2"
        amazon(a_url)
    

def flipkart(url):
    global page_number
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        b_headphones = soup.find("div", class_="_1YokD2 _3Mn1Gg").find_all(class_="_1AtVbE col-12-12")
        for b_headphone in b_headphones:
            checks = b_headphone.find_all("div", class_="_13oc-S")

            # elements = check.find_all('div', {'data-id': True})

            # for element in elements:
            for check in checks:
                check1 = check.find_all("div", class_="_4ddWXP")
                for check2 in check1:
                    # check available and offer
                    if not (check2.find("span", class_="_192laR")) and (check2.find("div", class_="_3Ay6Sb")):
                        
                        # data_asin = element['data-id']
                            # if data_asin:
                            #     fid.append(data_asin)

                        # Product Name List
                        FWHp = check2.find_all("a", class_="s1Q9rs")
                        for a_tag in FWHp:
                            title_attr = a_tag.get('title')
                            title_attr = str(title_attr)
                            title = title_attr.replace("/","").strip()
                            if(a_tag.findNext("div", class_="_3Djpdu")):
                                colorName = a_tag.findNext("div", class_="_3Djpdu").text
                                color = str(colorName)
                                color = color.replace("/","").strip()
                                fname.append(title+" "+color)
                            else:
                                fname.append(title)
                            link_attr = a_tag.get('href')
                            furl.append("https://flipkart.com"+str(link_attr))
                            # print("https://flipkart.com"+str(link_attr))

                        # Product Price List
                        price = check2.find_all("div", class_="_30jeq3")
                        for price1 in price:
                            price2 = price1.text.split("₹")[1]
                            price2 = str(price2)
                            price3 = price2.replace(",","")
                            fprice.append(price3)
                            # print(price3)

                        images = check2.find_all("img", class_="_396cs4")
                        # Product images
                        for image in images:
                            img = image["src"]
                            fimage.append(img)
                            # print(img)

                        offers = check2.find_all("div", class_="_3Ay6Sb")
                        # Product offer
                        for offer in offers:
                            off = offer.text
                            foffer.append(off)


        next_button = soup.find("a", {"class": "_1LKTO3"})
        if next_button is None:
            break

        page_number+=1
        url = "https://www.flipkart.com/search?q="+category+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+str(page_number)
        print(url)
    
    for i in furl:
        fid.append(fidFinder(i))

    print("--------------------------------------------------------------------------------------------------------------")
    print("Name",len(fname))
    print("Price",len(fprice))
    print("Offer",len(foffer))
    print("Image",len(fimage))
    print("Url",len(furl))
    print("Id",len(fid))
    print("--------------------------------------------------------------------------------------------------------------")
    fproduct_update(category,fname,fid,fprice,foffer,fimage,furl)
    

#-----------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------Product Category-------------------------------------------------#

categories=["Cameras","Wired Headphones","Bluetooth Headphones","Speakers","Pendrives","Mouses","Keyboards","Printers","Memory Cards","Projectors","Power Banks"]

for category in categories:

    aname.clear()
    aprice.clear()
    aoffer.clear()
    aimage.clear()
    aurl.clear()
    aid.clear()

    a_url="https://www.amazon.in/s?k="+category+"&page=1&ref=sr_pg_2"
    amazon(a_url)
        
    fname.clear()
    fprice.clear()
    foffer.clear()
    fimage.clear()
    furl.clear()
    fid.clear()
    page_number=1

    f_url="https://www.flipkart.com/search?q="+category+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"    
    flipkart(f_url)

    notification = Notify.objects.all()
    if(notification):
        for product in notification:
            asyncio.run(notify(product.name,product.price,product.image_link,product.offer,product.url))
            sleep(2)
            product.delete()

#--------------------------------------------------------------------------------------------------------------------#



def home(request):
    return render(request,"index.html")


# fname = ["Microflash S7-Deep Bass, Clear Hi-Fi Sound, Headphones Wired Headset Green, In the Ear","AXL AEP-15B-Black Wired Headset Black, In the Ear","Boult Audio Bassbuds X1 Wired Headset Black, In the Ear",]
# fprice = [1001,1001,1]
# fimage = ["https://rukminim1.flixcart.com/image/612/612/xif0q/headphone/n/d/0/s7-deep-bass-clear-hi-fi-sound-headphones-microflash-original-imaghe5fkvhucm9y.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/kzn17680/headphone/0/u/1/aep-15b-black-axl-original-imagbhsgt4v7yrvp.jpeg?q=70","https://rukminim1.flixcart.com/image/612/612/xif0q/headphone/f/7/7/-original-imagg5jypsfdsbjz.jpeg?q=70"]
# foffer = ["%901","%671","%581"]
# furl = ["https://flipkart.com/microflash-s7-deep-bass-clear-hi-fi-sound-headphones-wired-headset/p/itm15ad7438eacba?pid=ACCGHE5F8Q4G3YNZ&lid=LSTACCGHE5F8Q4G3YNZN9NXMM&marketplace=FLIPKART&store=0pm%2Ffcn&srno=b_20_764&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_3_L2_view-all&fm=organic&iid=en_nbCHtcELNojQavOWR%2FABw6ZJwKFTvGUx5Evq8IyEMRZjODsQaGh7AFJmmg0ATEsAW9c67JlbyN6WEGvJnCxe4w%3D%3D&ppt=None&ppn=None&ssid=b2gd96mw6o0000001681313223003","link22","link33"]


# Notify.objects.create(name="watch",price="100",offer="%10",url="flipkart.com",image_link="https://rukminim1.flixcart.com/image/612/612/xif0q/headphone/n/d/0/s7-deep-bass-clear-hi-fi-sound-headphones-microflash-original-imaghe5fkvhucm9y.jpeg?q=70")
        

# context = {'name': name[i],'price': price[i],'image':image[i],'link':"http://127.0.0.1:8000/collections/"+str(category)+"/"+product.name}
# def notification(request):
#     return render(request,"app/notification.html",context)


# def oneTwoPage(c_url):
#     # get current url
#     details_gathering(c_url)
#     # page move from 1 to 2
#     driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[2]/div[12]/div/div/nav/a[11]/span").click()
#     # get current url
#     c_url = driver.current_url
#     moveNextPage(c_url)


# def moveNextPage(c_url):
#     # next button
#     details_gathering(c_url)
#     response = requests.get(c_url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     if (soup.find("div", class_="_13oc-S")):
#         driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[2]/div[12]/div/div/nav/a[12]/span").click()
#         link = driver.current_url
#         moveNextPage(link)


# def details_gathering(c_url):

#     fname.clear()
#     fprice.clear()
#     foffer.clear()
#     fimage.clear()
#     furl.clear()

#     driver.get(c_url)
#     response = requests.get(c_url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     b_headphones = soup.find("div", class_="_1YokD2 _3Mn1Gg").find_all(class_="_1AtVbE col-12-12")
#     for b_headphone in b_headphones:
#         checks = b_headphone.find_all("div", class_="_13oc-S")
#         for check in checks:
#             check1 = check.find_all("div", class_="_4ddWXP")
#             for check2 in check1:
#                 # check available and offer
#                 if not (check2.find("span", class_="_192laR")) and (check2.find("div", class_="_3Ay6Sb")):
#                     # Product Name List
#                     FWHp = check2.find_all("a", class_="s1Q9rs")
#                     for a_tag in FWHp:
#                         title_attr = a_tag.get('title')
#                         title_attr = str(title_attr)
#                         title = title_attr.replace("/","")
#                         if(a_tag.findNext("div", class_="_3Djpdu")):
#                             colorName = a_tag.findNext("div", class_="_3Djpdu").text
#                             color = str(colorName)
#                             color = color.replace("/","")
#                             fname.append(title+" "+color)
#                         else:
#                             fname.append(title)
#                         link_attr = a_tag.get('href')
#                         furl.append("https://flipkart.com"+str(link_attr))
#                         print("https://flipkart.com"+str(link_attr))

#                     # Product Price List
#                     price = check2.find_all("div", class_="_30jeq3")
#                     for price1 in price:
#                         price2 = price1.text.split("₹")[1]
#                         price2 = str(price2)
#                         price3 = price2.replace(",","")
#                         fprice.append(price3)
#                         # print(price3)

#                     images = check2.find_all("img", class_="_396cs4")
#                     # Product images
#                     for image in images:
#                         img = image["src"]
#                         fimage.append(img)
#                         # print(img)

#                     offers = check2.find_all("div", class_="_3Ay6Sb")
#                     # Product offer
#                     for offer in offers:
#                         off = offer.text
#                         foffer.append(off)
#                     print("details successfully gathered")
#                 else:
#                     print("details not gather 1")

#     else:
#         print("details not gather 2")
                   
#     fproduct_update(category,fname,fprice,foffer,fimage,furl)


# def getLink(c_url):
#     driver.get(c_url)
#     product_elements = driver.find_elements(By.XPATH,"//div[@data-component-type='s-search-result']")
#     for product_element in product_elements:

#         if (product_element.find_elements(By.XPATH, ".//span[@class='a-price-whole']")):

#             name_element = product_element.find_element(By.XPATH,".//h2/a")
#             name = name_element.text
#             name = str(name)
#             name=name.replace("/","")

#             url = name_element.get_attribute("href")

#             price_element = product_element.find_element(By.XPATH,".//span[@class='a-price-whole']")
#             price = price_element.text
#             price = str(price).replace(",","")

#             image_element = product_element.find_element(By.XPATH,".//img")
#             image_link = image_element.get_attribute("src")

#             offer_element = product_element.find_element(By.XPATH, ".//div[@class='a-row a-size-base a-color-base']")
#             offer = offer_element.text.strip("")
#             offer = offer.split("(")[-1].replace(")","")
#             if "%" in offer:
#                 aname.append(name)
#                 aurl.append(url)
#                 aoffer.append(offer)
#                 aprice.append(price)
#                 aimage.append(image_link)

#     # source = requests.get(c_url, headers=headers)
#     # soup = BeautifulSoup(source.content, 'html.parser')
#     # isTrue = soup.find("a", class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")
#     next_button = driver.find_elements(By.CSS_SELECTOR,'.s-pagination-item.s-pagination-next.s-pagination-button')
#     if (next_button):
#         driver.find_element(By.XPATH, "//a[text()='Next']").click()
#         c_url = driver.current_url
#         getLink(c_url)
#     else:
#         aproduct_update(category,aname,aprice,aoffer,aimage,aurl)