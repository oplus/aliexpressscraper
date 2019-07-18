import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import re
import json
import bs4


alibrowser = webdriver.Firefox()
#url  = 'https://www.aliexpress.com/item/33011967786.html?spm=a2g0o.detail.1000060.3.7a8f6524cQnmMd&gps-id=pcDetailBottomMoreThisSeller&scm=1007.13339.99734.0&scm_id=1007.13339.99734.0&scm-url=1007.13339.99734.0&pvid=9394447d-07ff-4d13-bd55-f5e7d67cd62b'
url = "https://www.aliexpress.com/item/33015114480.html?spm=2114.search0103.3.10.13351a976a9BcO&ws_ab_test=searchweb0_0%2Csearchweb201602_9_10065_10068_319_10059_10884_317_10887_10696_321_322_10084_453_10083_454_10103_10618_10307_537_536%2Csearchweb201603_55%2CppcSwitch_0&algo_expid=aa0af252-781c-4e25-967d-a9dd8f06d9ba-1&algo_pvid=aa0af252-781c-4e25-967d-a9dd8f06d9ba"
#url = "https://www.aliexpress.com/item/32973661163.html?spm=a2g01.12617084.fdpcl001.5.2597b77Hb77Hlj&gps-id=5547572&scm=1007.19201.130907.0&scm_id=1007.19201.130907.0&scm-url=1007.19201.130907.0&pvid=34f94418-cefc-4fee-9609-84a8baff6737"



def log(msg):
    current_time = datetime.datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
    logging_message = msg + " @" + current_time + "\n"
    print(logging_message)
    with open("logging.txt", 'a+') as logging:
        logging.write(logging_message)

def force_render(browser):
    browser.maximize_window()
    browser.execute_script("window.scrollTo(0, 1080);")
    browser.execute_script("window.scrollTo(0, 0);")
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    log("Rendered all page")

def get_element(browser, by, selector):
    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((by, selector)))
        return element
    except TimeoutException:
        return None

def get_elements(browser, by, selector):
    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((by, selector)))
        return element
    except TimeoutException:
        return None

def get_product_page(browser, product_url):
    browser.get(product_url)
    log(f"Got product {product_url} page")
    disable_modal_ad(browser)
    force_render(browser)

def disable_modal_ad(browser): #Add testing for non presence
    by = By.CLASS_NAME
    selector = 'next-dialog-close'
    modal_ad = get_element(browser, by = by, selector = selector)
    if modal_ad:
        modal_ad.click()
        log("Disabled modal ad")
    else: log("Could not remove modal")




def get_product_disc(browser):
    by = By.CSS_SELECTOR
    selector = ".product-title"
    product_disc = get_element(browser, by = by, selector = selector)
    if product_disc:
        log(f"Got product discription: {product_disc.text}")
    else:log("Could not get product discription")


def get_store_name(browser):
    by = By.CSS_SELECTOR
    selector = '.store-info > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)'
    store_name = get_element(browser, by = by, selector = selector)
    if store_name:
        log(f"Got store name: {store_name.text}")
    else:log("Could not get store name")


def get_seller_rating(browser):
    by = By.CSS_SELECTOR
    selector = ".store-container > div:nth-child(2)"
    seller_rating = get_element(browser, by = by, selector = selector)
    if seller_rating:
        seller_rating = seller_rating.text.replace('\n', " ").strip()
        log(f"Got seller rating: {seller_rating}")
    else:log("Could not get seller rating")


def get_seller_followers(browser):
    by = By.CSS_SELECTOR
    selector = ".num-followers > i:nth-child(1)"
    seller_followers = get_element(browser, by = by, selector = selector)
    if seller_followers:
        log(f"Got seller followers: {seller_followers.text}")
    else:log("Could not get seller followers")


def get_product_rating(browser):
    by = By.CSS_SELECTOR
    selector = ".overview-rating-average"
    product_rating = get_element(browser, by = by, selector = selector)
    if product_rating:
        log(f"Got product rating: {product_rating.text}")
    else:log("Could not get product rating")


def get_number_reviews(browser):
    by = By.CSS_SELECTOR
    selector = ".product-reviewer-reviews"
    number_reviews = get_element(browser, by = by, selector = selector)
    if number_reviews:
        log(f"Got number of reviews: {number_reviews.text}")
    else:log("Could not get number of reviews")


def get_number_orders(browser):
    by = By.CSS_SELECTOR
    selector = ".product-reviewer-sold"
    number_orders = get_element(browser, by = by, selector = selector)
    if number_orders:
        log(f"Got number of orders: {number_orders.text}")
    else:log("Could not get number of orders")


def get_shipping_cost(browser):
    by = By.CSS_SELECTOR
    selector = ".product-shipping-price"
    shipping_cost = get_element(browser, by = by, selector = selector)
    if shipping_cost:
        log(f"Got shipping cost: {shipping_cost.text.strip('Shipping: ')}")
    else:log("Could not get shipping cost")


def get_shipping_time(browser):
    by = By.CSS_SELECTOR
    selector = ".product-shipping-delivery > span:nth-child(1)"
    shipping_time = get_element(browser, by = by, selector = selector)
    if shipping_time:
        log(f"Got shipping time: {shipping_time.text} days")
    else:log("Could not get shipping time")


def get_specs(browser):
    specs_tab = get_element(browser,
    by = By.CSS_SELECTOR,
    selector = ".detail-extend-tab > div:nth-child(1) > ul:nth-child(1) > li:nth-child(3) > div:nth-child(1) > span:nth-child(1)")
    if specs_tab:
        specs_tab.click()
    else:log("Could not click on specification tab")

    specs_data = get_element(browser,
    by = By.CSS_SELECTOR,
    selector = ".product-specs-list")

    DATA = {}
    if specs_data:
        for data in specs_data.text.split("\n"):
            DATA[data[:data.index(":")]] =  data[data.index(":")+1:].strip()
        log(f"Got specifications as follow:\n{DATA}")
    else:log("Could not get product specifications")


def get_recomm_urls(browser):
    recomm_urls = get_elements(browser,
    by = By.CSS_SELECTOR,
    selector = "a[ae_button_type='Seller_Recommendations']")
    if recomm_urls:
        DATA = [i.get_attribute("href") for i in recomm_urls]
        log(f"Got recommended urls:\n{DATA}")
    else:log("Could not get recommended urls")


def get_all_images(browser):
    dict_data = _get_json(browser)
    image_urls = dict_data["imageModule"]["imagePathList"]
    if image_urls:
        log(f"Got all product image urls:\n{image_urls}")
    else: log("Could not get product image urls.")


def get_price_variations(browser):
    dict_data = _get_json(browser)
    if dict_data:
        log(f"Got price variation combos:\n{_list_variations(dict_data)}")
    else:log("Could not get price combos.")











def _get_json(browser):
    source = browser.page_source
    soup = bs4.BeautifulSoup(source, "html.parser")
    json_data = re.search(r'data:.+"site":"glo"}}',  soup.text).group(0)[5:]
    dict_data = json.loads(json_data)
    return(dict_data)

def _prop_id_name(dict_data, id):
    for prop in dict_data["skuModule"]["productSKUPropertyList"]:
        for value in prop["skuPropertyValues"]:
            if value["propertyValueIdLong"] == id :
                return value["propertyValueDisplayName"]

def _list_variations(dict_data):
    price_variation_dict = {}
    price_list = dict_data["skuModule"]["skuPriceList"]
    for variation in price_list:
        props = [_prop_id_name(dict_data, int(id)) for id in variation["skuPropIds"].split(",")]
        currency = variation["skuVal"]["skuAmount"]["currency"]
        price = variation["skuVal"]["actSkuCalPrice"]
        availQty = variation["skuVal"]["availQuantity"]
        item = {",".join(props):{"price":price, "currency":currency, "availQty":availQty}}
        price_variation_dict.update(item)
    return (price_variation_dict, len(price_variation_dict))






#def get_all_product_images(browser):
#    source = browser.get_source()
#    print(source)




def scraper(browser, logging = True, ):


###############TESTING################
"""
get_product_page(alibrowser, url)
get_product_disc(alibrowser)
get_store_name(alibrowser)
get_seller_rating(alibrowser)
get_seller_followers(alibrowser)
get_product_rating(alibrowser)
get_number_reviews(alibrowser)
get_number_orders(alibrowser)
get_shipping_cost(alibrowser)
get_shipping_time(alibrowser)
get_specs(alibrowser)
get_recomm_urls(alibrowser)
get_all_images(alibrowser)
get_price_variations(alibrowser)
"""
