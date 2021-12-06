import base64
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Gaugan2Renderer:
    def __init__(self,):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def open(self):
        self.driver.get("http://gaugan.org/gaugan2/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "viewport"))
        )
        self.close_popups()

    def close_popups(self):
        close_button = self.driver.find_element(By.XPATH,
                                                "/html/body/div[2]/div/header/button")
        if close_button:
            close_button.click()

        terms_and_conditions = self.driver.find_element(
            By.XPATH, '//*[@id="myCheck"]')

        if terms_and_conditions:
            terms_and_conditions.click()

    def download_image(self, file_path):
        output_canvas = self.driver.find_element(
            By.ID, 'output')
        canvas_base64 = self.driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);", output_canvas)
        canvas_png = base64.b64decode(canvas_base64)

        with open(file_path, 'wb') as f:
            f.write(canvas_png)

    def create_output_dir(self):
        os.makedirs(self.output_path, exist_ok=True)

    def render_image(self, file_path):
        self.driver.find_element(
            By.XPATH, '//*[@id="segmapfile"]').send_keys(file_path)
        self.driver.find_element(
            By.XPATH, '//*[@id="btnSegmapLoad"]').click()
        self.driver.find_element(
            By.XPATH, '//*[@id="render"]').click()

    def run(self, file_paths, output_path):
        self.file_paths = file_paths
        self.output_path = output_path

        self.open()
        self.create_output_dir()

        for file_path in self.file_paths:
            basename = os.path.basename(file_path)
            print(f"Rendering {basename}")
            output_image = os.path.join(self.output_path,
                                        basename)

            self.render_image(file_path)
            time.sleep(10)
            self.download_image(output_image)

        self.driver.close()
