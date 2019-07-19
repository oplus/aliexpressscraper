import selenium
from selenium import webdriver
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import re
import json
import bs4




def log(msg, logging = True):
    """

    Parameters
    ----------
    msg : (str)
        log message to be printed on the screen and logged with time in file logging.txt.
    logging : (boolean)
        a boolean argument (True/False) which default is True. Use it when verbose is a
        demand by printing scraping steps and failures (if any).

    Returns
    -------
    None


    """
    if logging == True:
        current_time = datetime.datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
        logging_message = msg + " @" + current_time + "\n"
        print(logging_message)
        with open("logging.txt", 'a+') as logging:
            logging.write(logging_message)

def force_render(browser, logging = True):
    """AliExpress product page does not render completely unless it is scrolled up/down
    and to make sure all data points are vaisible to mainScraper this function zoom out
    from css content.


    Parameters
    ----------
    browser : (webdriver instance)
        Selenium webdriver instance

    logging : (boolean)
        A boolean argument (True/False) which default is True. Use it when verbose is a
        demand by printing scraping steps and failures (if any).


    Returns
    -------
    None


    """
    browser.maximize_window()
    browser.execute_script("window.scrollTo(0, 1080);")
    browser.execute_script("window.scrollTo(0, 0);")
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    browser.find_element_by_tag_name("html").send_keys(Keys.CONTROL,Keys.SUBTRACT)
    log("Rendered all page", logging)

def get_element(browser, by, selector):
    """use WebDriverWait method to wait for 10 seconds for an element to load on the page


    Parameters
    ----------
    browser : (webdriver instance)
        Selenium webdriver instance to
    by : (selenium.webdriver.common.by.By  instance)
        Set of supported locator strategies that tells the borwser which strategy to use in
        finding an element (CLASS_NAME, XPATH, CSS_SELECTOR)
    selector : (str)
        A string representing the element selector from the DOM whichever xpath, class name
        or css selector.

    Returns
    -------
    (Webdrive element)
        A found element which can be processed later by procedures such as .click() and
        has attributes such as .text which represent the innerHTML text of an element.

    """
    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((by, selector)))
        return element
    except TimeoutException:
        return None

def get_elements(browser, by, selector):
    """use WebDriverWait method to wait for 10 seconds for an element to load on the page


    Parameters
    ----------
    browser : (webdriver instance)
        Selenium webdriver instance
    by : (selenium.webdriver.common.by.By  instance)
        Set of supported locator strategies that tells the borwser which strategy to use in
        finding an element (CLASS_NAME, XPATH, CSS_SELECTOR)
    selector : (str)
        A string representing the element selector from the DOM whichever xpath, class name
        or css selector.

    Returns
    -------
    (List of Webdrive element)
        A found elements which can be processed later by procedures such as .click() and
        has attributes such as .text which represent the innerHTML text of an element.

    """
    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((by, selector)))
        return element
    except TimeoutException:
        return None

def get_product_page(browser, product_url, logging = True):
    """A function that opens the product url in the browser instance created previously
    and passed to the same function

    Parameters
    ----------
    browser : (webdriver instance)
        Selenium webdriver instance
    product_url : (str)
        The product page url.
    logging : (boolean)
        A boolean argument (True/False) which default is True. Use it when verbose is a
        demand by printing scraping steps and failures (if any).

    Returns
    -------
    None
        It returns None, however it brings up the browser instance to the product url
        to be ready for scraping.

    """
    browser.get(product_url)
    log(f"Got product {product_url} page", logging)
    disable_modal_ad(browser, logging)
    force_render(browser, logging)

def disable_modal_ad(browser, logging = True):
    """A function that check/disable the modal ad which covers the dom and prevent the
    script from interacting with the webpage

    """
    by = By.CLASS_NAME
    selector = 'next-dialog-close'
    modal_ad = get_element(browser, by = by, selector = selector)
    if modal_ad:
        modal_ad.click()
        log("Disabled modal ad", logging)
    else: log("No modal ad encountered", logging)




def get_product_disc(browser, logging = True):
    """A function that search for the product discription in the product page and return
    it
    """
    by = By.CSS_SELECTOR
    selector = ".product-title"
    product_disc = get_element(browser, by = by, selector = selector)
    if product_disc:
        log(f"Got product discription: {product_disc.text}", logging)
        return product_disc.text
    else:
        log("Could not get product discription", logging)
        return None


def get_store_name(browser, logging = True):
    """A function that search for the store name in the product page and return
    it
    """
    by = By.CSS_SELECTOR
    selector = '.store-info > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)'
    store_name = get_element(browser, by = by, selector = selector)
    if store_name:
        log(f"Got store name: {store_name.text}", logging)
        return store_name.text
    else:
        log("Could not get store name", logging)
        return None


def get_seller_rating(browser, logging = True):
    """A function that search for the seller rating in the product page and return
    the percentage only (e.g. 98%)
    """
    by = By.CSS_SELECTOR
    selector = ".store-container > div:nth-child(2)"
    seller_rating = get_element(browser, by = by, selector = selector)
    if seller_rating:
        seller_rating = seller_rating.text.replace('\n', " ").strip()
        seller_rating = re.search(r"\d{1,3}.?\d{0,3}%",seller_rating).group(0)
        log(f"Got seller rating: {seller_rating}", logging)
        return seller_rating
    else:
        log("Could not get seller rating", logging)
        return None


def get_seller_followers(browser, logging = True):
    """A function that search for number of seller followers in the product page and return
    it
    """
    by = By.CSS_SELECTOR
    selector = ".num-followers > i:nth-child(1)"
    seller_followers = get_element(browser, by = by, selector = selector)
    if seller_followers:
        log(f"Got seller followers: {seller_followers.text}", logging)
        return seller_followers.text
    else:
        log("Could not get seller followers", logging)
        return None


def get_product_rating(browser, logging = True):
    """A function that search for the product rating in the product page and return
    it
    """
    by = By.CSS_SELECTOR
    selector = ".overview-rating-average"
    product_rating = get_element(browser, by = by, selector = selector)
    if product_rating:
        log(f"Got product rating: {product_rating.text}", logging)
        return product_rating.text
    else:
        log("Could not get product rating", logging)
        return None


def get_number_reviews(browser, logging = True):
    """A function that search for number of reviews in the product page and return
    it
    """
    by = By.CSS_SELECTOR
    selector = ".product-reviewer-reviews"
    number_reviews = get_element(browser, by = by, selector = selector)
    if number_reviews:
        log(f"Got number of reviews: {number_reviews.text}", logging)
        return number_reviews.text
    else:
        log("Could not get number of reviews", logging)
        return None



def get_number_orders(browser, logging = True):
    """A function that search for number of orders in the product page and return
    it
    """
    by = By.CSS_SELECTOR
    selector = ".product-reviewer-sold"
    number_orders = get_element(browser, by = by, selector = selector)
    if number_orders:
        log(f"Got number of orders: {number_orders.text}", logging)
        return number_orders.text
    else:
        log("Could not get number of orders", logging)
        return None


def get_shipping_cost(browser, logging = True):
    """A function that search for the shipping cost in the product page and return
    it. This value depend on the country of scraping device.
    """
    by = By.CSS_SELECTOR
    selector = ".product-shipping-price"
    shipping_cost = get_element(browser, by = by, selector = selector)
    if shipping_cost:
        shipping_cost = shipping_cost.text.strip('Shipping: ')
        log(f"Got shipping cost: {shipping_cost}", logging)
        return shipping_cost
    else:
        log("Could not get shipping cost", logging)
        return None


def get_shipping_time(browser, logging = True):
    """A function that search for estimated shipping duration in the product page and return
    it. This value depend on the country of scraping device.
    """
    by = By.CSS_SELECTOR
    selector = ".product-shipping-delivery > span:nth-child(1)"
    shipping_time = get_element(browser, by = by, selector = selector)
    if shipping_time:
        log(f"Got shipping time: {shipping_time.text} days", logging)
        return shipping_time.text
    else:
        log("Could not get shipping time", logging)
        return None


def get_specs(browser, logging = True):
    """A function clicks on the specifications tab in the product page to show/scrape all specs
    and return them as a python dictionary
    """
    #Find specs tab and click on it
    specs_tab = get_element(browser,
    by = By.CSS_SELECTOR,
    selector = ".detail-extend-tab > div:nth-child(1) > ul:nth-child(1) > li:nth-child(3) > div:nth-child(1) > span:nth-child(1)")
    if specs_tab:
        specs_tab.click()
    else:log("Could not click on specification tab", logging)
    #Find all specs keys/values and return them in a dictionary
    specs_data = get_element(browser,
    by = By.CSS_SELECTOR,
    selector = ".product-specs-list")
    DATA = {}
    if specs_data:
        for data in specs_data.text.split("\n"):
            DATA[data[:data.index(":")]] =  data[data.index(":")+1:].strip()
        log(f"Got specifications as follow:\n{DATA}", logging)
        return DATA
    else:
        log("Could not get product specifications", logging)
        return None


def get_recomm_urls(browser, logging = True):
    """A function that search for recommended urls in the product page and return them in a list
    """
    recomm_urls = get_elements(browser,
    by = By.CSS_SELECTOR,
    selector = "a[ae_button_type='Seller_Recommendations']")
    if recomm_urls:
        DATA = [i.get_attribute("href") for i in recomm_urls]
        log(f"Got recommended urls:\n{DATA}", logging)
        return DATA
    else:
        log("Could not get recommended urls", logging)
        return None


def get_all_images(browser, logging = True):
    """A function that search for all product images urls in the product page and return them in a list
    """
    dict_data = _get_json(browser)
    image_urls = dict_data["imageModule"]["imagePathList"]
    if image_urls:
        log(f"Got all product image urls:\n{image_urls}", logging)
        return image_urls
    else:
        log("Could not get product image urls.", logging)
        return None


def get_price_variations(browser, logging = True):
    """A function that combine product variations along with price and availability and return then as
    a python dictionary
    """
    dict_data = _get_json(browser)
    if dict_data:
        combos = _list_variations(dict_data)
        log(f"Got price variation combos:\n{combos}", logging)
        return combos
    else:
        log("Could not get price combos.", logging)
        return None











def _get_json(browser):
    """Helper function that search in the page source for the josn object conataining all product variations/prices/availability
    and return a python dictionary deserlized from this json object.
    """
    source = browser.page_source
    soup = bs4.BeautifulSoup(source, "html.parser")
    json_data = re.search(r'data:.+"site":"glo"}}',  soup.text).group(0)[5:]
    dict_data = json.loads(json_data)
    return(dict_data)

def _prop_id_name(dict_data, id):
    """A function that transform product property id to property name as each product property
    is stored in the json data object as and id(e.g. _prop_id_name(dict_data, 137)) returns Black
    as BLACK is the property of id 137
    """
    for prop in dict_data["skuModule"]["productSKUPropertyList"]:
        for value in prop["skuPropertyValues"]:
            if value["propertyValueIdLong"] == id :
                return value["propertyValueDisplayName"]

def _list_variations(dict_data):
    """A function that uses the scraped json object to list all product combos/price and availability and
    return them as a python dictionary
    """
    price_variation_dict = {}
    price_list = dict_data["skuModule"]["skuPriceList"]
    for variation in price_list:
        props = [_prop_id_name(dict_data, int(id)) for id in variation["skuPropIds"].split(",")]
        currency = variation["skuVal"]["skuAmount"]["currency"]
        price = variation["skuVal"]["actSkuCalPrice"]
        availQty = variation["skuVal"]["availQuantity"]
        item = {",".join(props):{"price":price, "currency":currency, "availQty":availQty}}
        price_variation_dict.update(item)
    return (price_variation_dict)


def mainScraper(browser, url, logging):
    """A function that combine all data points and scrape them at once returning one python dictionary
    including all available data points from the product page

    Parameters
    ----------
    browser : (webdriver instance)
        Selenium webdriver instance
    url : (str)
        The product page url.
    logging : (boolean)
        A boolean argument (True/False) which default is True. Use it when verbose is a
        demand by printing scraping steps and failures (if any).

    Returns
    -------
    (dict)
        A python dictionary that include all data points structured as per PRODUCT_DATA dictionary below
    """
    get_product_page(browser, url, logging)
    PRODUCT_DATA = {
    "product_description":get_product_disc(browser, logging),
    "store_name":get_store_name(browser, logging),
    "seller_rating":get_seller_rating(browser, logging),
    "seller_followers":get_seller_followers(browser, logging),
    "product_rating":get_product_rating(browser, logging),
    "number_of_reviews":get_number_reviews(browser, logging),
    "number_of_orders":get_number_orders(browser, logging),
    "shipping_cost":get_shipping_cost(browser, logging),
    "shipping_duration":get_shipping_time(browser, logging),
    "product_specs":get_specs(browser, logging),
    "recommended_urls":get_recomm_urls(browser, logging),
    "product_images":get_all_images(browser, logging),
    "product_variations":get_price_variations(browser,logging)
    }

    return PRODUCT_DATA
