import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:/chromedriver/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_show_all_pets():
    pytest.driver.find_element(By.ID, 'email').send_keys('mastashake1@mail.ru')

    pytest.driver.find_element(By.ID,'pass').send_keys('m1lkshake')

    pytest.driver.implicitly_wait(10)

    pytest.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()

    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    images = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
    names = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    descriptions = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ages[i].text != ''



def test_show_my_pets():
    pytest.driver.find_element(By.ID, 'email').send_keys('mastashake1@mail.ru')
    pytest.driver.find_element(By.ID,'pass').send_keys('m1lkshake')
    pytest.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()


    assert WebDriverWait(pytest.driver, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

    pytest.driver.find_element(By.CLASS_NAME, 'navbar-toggler').click()

    pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    assert WebDriverWait(pytest.driver, 5).until(EC.text_to_be_present_in_element((By.ID, 'all_my_pets'), "All"))

    data_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr')

    for i in range(len(data_my_pets)):
        assert WebDriverWait(pytest.driver, 5).until(EC.visibility_of(data_my_pets[i]))

    image_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            assert WebDriverWait(pytest.driver, 5).until(EC.visibility_of(image_my_pets[i]))

    name_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    for i in range(len(name_my_pets)):
        assert WebDriverWait(pytest.driver, 5).until(EC.visibility_of(name_my_pets[i]))

    type_my_pets = pytest.driver.find_elements(By.XPATH,'//tbody/tr/td[2]')
    for i in range(len(type_my_pets)):
        assert WebDriverWait(pytest.driver, 5).until(EC.visibility_of(type_my_pets[i]))

    age_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
    for i in range(len(age_my_pets)):
        assert WebDriverWait(pytest.driver, 5).until(EC.visibility_of(age_my_pets[i]))

    all_statistics = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
    statistics_pets = all_statistics[1].split(" ")
    all_my_pets = int(statistics_pets[-1])

    assert len(data_my_pets) == all_my_pets

    count = 0
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            count += 1
    assert count >= all_my_pets / 2

    for i in range(len(name_my_pets)):
        assert name_my_pets[i].text != ''

    for i in range(len(type_my_pets)):
        assert type_my_pets[i].text != ''

    for i in range(len(age_my_pets)):
        assert age_my_pets[i].text != ''

    list_name_my_pets = []
    for i in range(len(name_my_pets)):
        list_name_my_pets.append(name_my_pets[i].text)
    set_name_my_pets = set(list_name_my_pets)
    assert len(list_name_my_pets) == len(set_name_my_pets)

    list_data_my_pets = []
    for i in range(len(data_my_pets)):
        list_data = data_my_pets[i].text.split("\n")

        list_data_my_pets.append(list_data[0])
    set_data_my_pets = set(list_data_my_pets)
    assert len(list_data_my_pets) == len(set_data_my_pets)