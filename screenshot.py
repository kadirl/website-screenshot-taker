from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import chromedriver_autoinstaller
import time
import traceback
from selenium import webdriver

chromedriver_autoinstaller.install()

class Screenshot:
    def __init__(self, *, driver=None, size={"width": 1920, "height": 1200}, scale_factor=1, dark_mode=False, wait_time=60, freeze_page=False):
        # init driven if not provided
        if driver is None:
            options = ChromeOptions()

            options.add_argument("--start-maximized")
            options.add_argument("--disable-extensions")
            options.add_argument("--headless")
            options.add_argument('--disable-cookies')
            options.add_argument('--high-dpi-support=1')
            options.add_argument('--disable-gpu')
            options.add_argument(f'--force-device-scale-factor={scale_factor}')
            options.add_argument('--disable-site-isolation-trials')
            options.page_load_strategy = "none"
            experimentalFlags = ['calculate-native-win-occlusion@2']
            chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
            options.add_experimental_option('localState',chromeLocalStatePrefs)
            driver = webdriver.Chrome(options=options)

        # setup color scheme
        if dark_mode:
            driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-color-scheme", "value": "dark"}]})

        # setup driver scaling
        driver.set_window_size(size['width'], size['height'])

        # assign everything
        self.driver = driver
        self.size = size
        self.scale_factor = scale_factor
        self.dark_mode = dark_mode
        self.wait_time = wait_time
        self.freeze_page = freeze_page


    def _open(self, url):

        self.driver.set_page_load_timeout(self.wait_time)
        self.driver.set_script_timeout(self.wait_time)

        # Openning a website
        self.driver.get(url)

        # Wait until the document is ready
        try:
            wait = WebDriverWait(self.driver, self.wait_time)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
            return True
        except TimeoutException as e:
            logging.warning('TIMEDOUT')
            return False


    def _reset_window_size(self):
        self.driver.set_window_size(self.size['width'], self.size['height'])


    def _hide_scrollbar(self):
        # CSS to hide scrollbar on screenshots
        css = """
            *::-webkit-scrollbar { display: none !important; }
            * { -ms-overflow-style: none !important; scrollbar-width: none !important; }
        """
        # CSS injection
        self.driver.execute_script(f"var style = document.createElement('style'); style.innerHTML = `{css}`; document.head.appendChild(style);")


    def _freeze_units(self):
        with open('freeze_units.js', 'r') as file:
            self.driver.execute_script(file.read())

    
    def _remove_scroll_listeners(self):
        self.driver.execute_script('let body = document.getElementsByTagName("body")[0]; body.replaceWith(body.cloneNode(true))')


    def _prepare_webpage(self, custom_size={}):

        # Getting & reseting the resolution
        window_width, window_height = custom_size.values() or self.size.values()
        self.driver.set_window_size(window_width, window_height)

        # Waiting for animations to complete before freezing
        time.sleep(2)
        
        # Preparing to take screenshot
        self._hide_scrollbar()

        self.driver.execute_script("document.getElementsByTagName('html')[0].style.setProperty('scroll-behavior', 'smooth', 'important');")
        max_page_height = self.driver.execute_script("return document.body.scrollHeight;")
        self.driver.execute_script(f"innerHeight = -99999")
        self.driver.execute_script(f"window.scrollTo(0, {max_page_height});")
        time.sleep(4)
        self.driver.execute_script(f"window.scrollBy(0, -48)")
        time.sleep(1)


        # Removing all event listeners to turn off any scroll animations
        self._remove_scroll_listeners() ########################################
        time.sleep(4)

        # Scrolling to the bottom
        self.driver.execute_script(f"window.scrollTo(0, 0);")
        time.sleep(2)

        # Freezing dimensions
        if self.freeze_page:
            self._freeze_units()
        
        # Setting the window size equal to page size
        max_page_height = max(self.size['height'], self.driver.execute_script("return document.body.scrollHeight;"))
        self.driver.set_window_size(window_width, max_page_height)

        # Waiting to everything to end
        time.sleep(1)


    def get_fullpage_screensho_as_base64(self, url, size={}):
        status = self._open(url)
        self._prepare_webpage(custom_size=size)
        screenshot =  self.driver.get_screenshot_as_base64()
        self._reset_window_size()
        return screenshot, status


    def get_fullpage_screenshot_as_png(self, url, size={}):
        status = self._open(url)
        self._prepare_webpage(custom_size=size)
        screenshot = self.driver.get_screenshot_as_png()
        self._reset_window_size()
        return screenshot, status


    def get_fullpage_screenshot_as_file(self, url, filename, size={}):
        status = self._open(url)
        if not status:
            filename = ''.join(filename.split('.')[:-1]) + '_TIMED_OUT.png'
        self._prepare_webpage(custom_size=size)
        self.driver.get_screenshot_as_file(filename)
        self._reset_window_size()
        return status

        
    def __del__(self):
        self.driver.quit()

if __name__ == '__main__':
    # url to test
    url = 'https://insomnia.rest/changelog'

    sc_chrome_freezed = Screenshot(size={'width': 1920, 'height': 1200}, scale_factor=2, freeze_page=True, wait_time=300)
    sc_chrome_freezed.get_fullpage_screenshot_as_file(url, 'test' + str(time.time()) + '.png')
    print('chrome scaled fixed done')
    del sc_chrome_freezed

