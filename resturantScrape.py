
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
import csv
import time

class TripAdvisorData:
    def __init__(self,url,driver,wait):
        self.driver=driver
        self.wait=wait
        self.url=url
        self.resturant_review_link_list=[]
        
        
        
    #method to get resturant review link from tripadvisor
        
    def get_review_link(self):
    
        self.driver.get(self.url)
        try:
            #selecting the element that has number of resturnat info using selenium
            resturants_list_column=self.wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div")))
            try:
                #getting the inner html data present in the column
                html_content=resturants_list_column.get_attribute("innerHTML")
                try:
                    #beautifulsoup library for parsing html 
                    all_resurant_review_link_list=BeautifulSoup(html_content,"html.parser")
                    #find all the review link 
                    for review_link in all_resurant_review_link_list.find_all("a",class_="review_count"):
                        additional_link=review_link['href']
                        if (additional_link.split("-")[0])!="/Hotel_Review":
                        # self.resturant_all_information(additional_link)
                            try:
                                #saving the link into file
                                self.write_into_file("IndianResturalURL.txt",additional_link)
                            except Exception as E:
                                print(f"Error:: {E}")
                    
                except Exception as e:
                    print(e) 
                    print("BeautifulSoup parsing not sucessfull")
            except Exception as e:
                print(e)
                print("Inner html data not found")    
        
        except Exception as e:
            
            
            print("element not found ")
        time.sleep(5)
       
        
        
            
        
      #method to extract the resturant information  
    
    def resturant_all_information(self,additional_link):
            
        try:
            #selenium driver to got the exact link to extract info
                self.driver.get(f"https://www.tripadvisor.com{additional_link}")
                print(additional_link)
                try:
                    main_content_element=self.wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div[2]")))
                    # print("Main Content")
                    html_content=main_content_element.get_attribute("innerHTML")
                    try:
                        each_resturant_content=BeautifulSoup(html_content,"html.parser")
                        try:
                            #extracting resturant name
                            resturant_name=each_resturant_content.find("h1").text
                        
                        except Exception as e:
                            print(e)
                            print("Resturant Name not found")
                            resturant_name=None
                        # print(resturant_name.text)
                        try:
                            #getting cusine names
                            cusine_div=each_resturant_content.find_all("div",class_="SrqKb")[1]
                            cusine_name=cusine_div.text
                            
                            print(cusine_name)
                            
                            
                            
                        except :
                            print("cusine_name not found")
                            cusine_name=None
                            
                        # print("cusine name",cusine_name)
                        try:
                            #container that has list of reivews 
                            for val in (each_resturant_content.find("div",class_="listContainer hide-more-mobile").find_all("div",class_="review-container")):
                                   #getting span that has rating value information
                                    try:
                                        #getting rating span 
                                        rating_span=val.find("div",class_="ui_column is-9").find("span")
                                        #getting the numeric value from the class name to find out the rating number
                                        rating_value=int(rating_span['class'][-1].split("_")[-1])/10
                                        # print("rating",rating_value)
                                        
                                    except Exception as e:
                                        print(e)
                                        print("rating value not found")
                                        rating_value=0
                                    try:
                                        #exracting review written date
                                        review_date=val.find("span",class_="ratingDate").text
                                    
                                    except Exception as e:
                                        print(e)
                                        print("review date not found")
                                        review_date=None
                                    
                                    try:
                                        #each reivew titile quote 
                                        review_quote=val.find("span",class_="noQuotes").text
                                    except:
                                        print("Review quote not found")
                                        review_quote=None
                                    try:
                                        #detail information of the review
                                        detail_review=val.find("p",class_="partial_entry").text
                                    except :
                                        print("Detail Review not found")
                                        detail_review=None
                                        # review_link_list.append({})
                                    
                                    try:
                                        # print(type(rating_value))
                                        #writing extracted data into the csv file
                                        self.write_into_csv_file("IndiaResturantData.csv",[resturant_name,cusine_name,review_date,review_quote,detail_review,rating_value])
                                    
                                    
                                        pass
                                        
                                            
                                    except Exception as e:
                                        print(e)
                                        print("Csv File Writing not Sucessfull")
                                    # whole_resturant_data={'Name':resturant_name,"Cusine":cusine_name,"Review_Date":review_date,"Review_Quote":review_quote,"Detail_Review":detail_review,"Review_Rating":rating_value}
                                    # print(whole_resturant_data)
                        
                                    
                                    
                                
                                
                        except Exception as e:
                            print(e)
                            print("Container Class not found")
                            # print("Additional info ",additional_link)
                                
                
                    except :
                        print("Error in Beautiful Soup Scaraping")
            
                    
                except Exception as e:
                    print(e)
                    print("Element not found ")
        except Exception as e:
            print(e)
            print("invalid url ")
        #sleep timing for driver 
        time.sleep(5)
            
        
    def write_into_file(self,filename,list_of_data):
        with open(filename,"a+") as file:
            file.write(list_of_data+"\n")
            
    def write_into_csv_file(self, filename, list_of_data=[]):
        with open(filename, mode="a+", newline="\n") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(list_of_data)
        
        
if __name__=="__main__":
    #setting up chorme extension
    try:
        # using already opened firefox to run the driver
        firefox_services = Service(port=5634, service_args=['--marionette-port', '2828', '--connect-existing'])
        driver = Firefox(service=firefox_services)
    except Exception as e :
        print(f"Error :: {e}")
    #driver waitig time initialization
    wait=WebDriverWait(driver,5)
    #code get the review link of the each resturant based on the location
    # for offset_Val in range(0,360,30):
        
    #     #url with offset value to get more data in other page number
    #     #gecode for nepal and india to get resturant list
    #     # geo_code=293860,293889
    #     url=f"https://www.tripadvisor.com/Search?geo=293860&q=resturant&queryParsed=true&searchSessionId=001a7ab41138f2c4.ssid&searchNearby=false&sid=DA70EAF89BEF93567F47927DC77972471697382226479&blockRedirect=true&ssrc=m&rf=7&o={offset_Val}"
    
    #     obj=TripAdvisorData(url,driver,wait)
        
    #     obj.get_review_link()
    
    #code to etract review details using the link saved in the csv file
    with open("IndianResturalUrl.txt","r") as file:
        lines=file.readlines()
        obj=TripAdvisorData("",driver,wait)
        for each_link in lines:
            additional_link=(each_link.strip())
            print("next line")
            # print(additional_link)
            obj.resturant_all_information(additional_link=additional_link)
            
            
        
          
    #     pass
    
    
    
        #print(obj.resturant_review_link_list)
       
    # print(obj.resturant_review_link_list)
    
    # print(len(obj.resturant_review_link_list))
    #     # break
        # self.driver=Firefox()
    #     print(offset_Val)
        # # print(url)
    # https://www.tripadvisor.com/
    # url=f'https://www.tripadvisor.com/'
        
    # url="https://www.tripadvisor.com/"
        # print("driver set up")
        # self.wait=WebDriverWait(self.driver,10)
        
        # (self.driver.get(self.url))
        
        # # print(self.driver)
    # # "https://www.tripadvisor.com/Search?searchSessionId=0003b7ca281e41bd.ssid&ssrc=e&q=resturant&sid=DA70EAF89BEF93567F47927DC77972471697379760520&blockRedirect=true&isSingleSearch=true&geo=293889&queryParsed=true&rf=1"
    
    # def get_max_offset_value(self):
            # print("additional link :: ",each_resturant_additional_link)
    # print(obj.get_max_offset_value())
    #     max_offset_val=0
    #     # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #     page_number=self.wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[2]/div/div/div/div")))
    #     page_number_soup=BeautifulSoup((page_number.get_attribute("innerHTML")))
    #     for val in (page_number_soup.find_all("a")):
    #         int_offset=int((val['data-offset']))
    #         print(type(int_offset))
    #         if int_offset>max_offset_val:
    #             max_offset_val=int_offset
    #     return max_offset_val
        
        # print
        # all_handles=self.driver.window_handles
        # new_tab=all_handles[1]
        
        # print("tab len",(new_tab),type(new_tab))
         
        
        # print(search_resturant,self.driver.current_url)
        # self.driver.switch_to.window(new_tab)
        # print(self.driver.current_url)
        
        # main_scrapable_content=self.wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]")))
        # scrapable_content=(main_scrapable_content.get_attribute("innerHTML"))
        
        
        # Scraped_content=BeautifulSoup(scrapable_content,"html.parser")
        # print(Scraped_content)
        
        # print("enterning value")
        # resturant_search_button=self.wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/main/div[4]/div/div/div[2]/div/form/div/span/button")))
        # print("pressing button")
        # resturant_search_button.click()
        
       
        
        # search_resturant=self.wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]")))
        # print("searching")
        # search_resturant.click()
        # time.sleep(10)
        # print(resturants_list_column)
        
                
        
        # whole_resturant_data={}
        # Review_list=[]
        # review_link_list=["https://www.tripadvisor.com/Restaurant_Review-g293891-d7226197-Reviews-Namaste_Air_Nandoj_Restaurant_Bar-Pokhara_Gandaki_Zone_Western_Region.html",
        #                   "https://www.tripadvisor.com/Hotel_Review-g293890-d1932602-Reviews-Bag_Packer_s_Lodge-Kathmandu_Kathmandu_Valley_Bagmati_Zone_Central_Region.html"]
        # for each_resturant_additional_link in self.resturant_review_link_list:
            
            # self.driver.get(f"https://www.tripadvisor.com{each_resturant_additional_link}")