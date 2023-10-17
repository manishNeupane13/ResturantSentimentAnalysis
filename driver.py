# from selenium.webdriver.firefox.options import Options
# from selenium import webdriver
# # options = Options()
# # caps = webdriver.DesiredCapabilities().FIREFOX
# # caps["marionette"] = True
# # drivePath = r 'C:\\Users\\geckodriver.exe' 
# driver = webdriver.Firefox()
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
options=Options()
options.log_path="geckodriver.log"
options.log_level="INFO"
options.add_argument("-profile F:\\Admin\\resturantReviewInternship\\ResturantSentimentAnalysis\\firefox_profile")
# options.arguments("-profile F:\Admin\resturantReviewInternship\ResturantSentimentAnalysis\firefox_profile")

firefox_services = Service(port=5634, service_args=['--marionette-port', '2828', '--connect-existing'])
driver = webdriver.Firefox(service=firefox_services,options=options)
driver.get('https://youtube.com')
# driver.execute_script('alert(\'your favorite music is here\')')