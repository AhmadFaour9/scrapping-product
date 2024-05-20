#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import csv
import json

# تعريف الكائن الذي يمثل المنتج
class Product:
    def __init__(self, name, price, description, specifications, rating):
        self.name = name
        self.price = price
        self.description = description
        self.specifications = specifications
        self.rating = rating

# جمع معلومات المنتجات من موقع أمازون
def amazon(products):
    url = 'https://www.amazon.com/s?k=laptop'

    # إطلاق متصفح الويب (Chrome) باستخدام Selenium
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)
    # انتظار تحميل نتائج البحث واستخراج البيانات باستخدام BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    laptops = soup.find_all('div', {'data-component-type': 's-search-result'})

    for laptop in laptops:
        name = laptop.find('span', {'class': 'a-size-medium'})
        if name is not None:
            name = name.text.strip()
        else:
            name = 'N/A'

        price = laptop.find('span', {'class': 'a-offscreen'})
        if price is not None:
            price = price.text.strip()
        else:
            price = 'N/A'

        rating = laptop.find('span', {'class': 'a-icon-alt'})
        if rating is not None:
            rating = rating.text.split()[0]
        else:
            rating = 'N/A'

        link = laptop.find('a', {'class': 'a-link-normal'})
        if link is not None:
            link = 'https://www.amazon.com' + link['href']
            driver.get(link)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            description_elem = soup.find('div', {'id': 'productDescription'})
            if description_elem is not None:
                description = description_elem.text.strip()
            else:
                description = 'N/A'
            specifications_elem = soup.find_all('div', {'class': 'a-section a-spacing-small'})
            if specifications_elem:
                specifications_list = []
                for spec in specifications_elem:
                    if 'product information' in spec.text.lower():
                        continue
                    spec_name_elem = spec.find('th')
                    if spec_name_elem is not None:
                        spec_name = spec_name_elem.text.strip()
                    else:
                        spec_name = 'N/A'
                    spec_value_elem = spec.find('td')
                    if spec_value_elem is not None:
                        spec_value = spec_value_elem.text.strip()
                    else:
                        spec_value = 'N/A'
                    specifications_list.append(f'{spec_name}: {spec_value}')
                specifications = '\n'.join(specifications_list)
            else:
                specifications = 'N/A'
        else:
            description = 'N/A'
            specifications = 'N/A'

        product = Product(name, price, rating, description, specifications)
        products.append(product)

    # إغلاق المتصفح
    driver.quit()

# جمع معلومات المنتجات من موقع laptop.sy
def laptopsy(products):        
    url = 'https://laptop.sy/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    laptops = soup.find_all('div', class_='fusion-product-content')

    for laptop in laptops:
        name = laptop.a.text
        price = laptop.span.text
        link = laptop.a['href']
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        description_elem = soup.find('div', class_='fusion-product-description')
        if description_elem is not None:
            description = description_elem.text.strip()
        else:
            description = 'N/A'
        specifications_elem = soup.find('div', {'id': 'tab-additional_information'})
        if specifications_elem is not None:
            specifications = specifications_elem.find_all('tr')
            specifications_list = []
            for spec in specifications:
                key_elem = spec.find('th')
                if key_elem is not None:
                    key = key_elem.text.strip()
                    value_elem = spec.find('td')
                    if value_elem is not None:
                        value = value_elem.text.strip()
                        specifications_list.append(f'{key}: {value}')
            # إضافة معلومات اللابتوب إلى المواصفات
            laptop_info = f"Laptop Name: {name}\nPrice: {price}\nLink: {link}"
            specifications_list.append(laptop_info)
            specifications = '\n'.join(specifications_list)
        else:
            specifications = 'N/A'
        rating_elem = soup.find('span', {'class': ['rating', 'review-stars-text']})
        if rating_elem is not None:
            rating = rating_elem.text.strip()
        else:
            rating = 'N/A'
        product = Product(name, price, description, specifications, rating)
        products.append(product)

# حفظ المعلومات المجمعة في ملف CSV أو JSON
def save_products(products, file_type):
    # تعريف أسماء الحقول
    field_names = ['name', 'price', 'description', 'specifications', 'rating']

    # تعريف اسم الملف بناءً على نوع الملف
    if file_type == 'csv':
        file_name = 'products.csv'
    elif file_type == 'json':
        file_name = 'products.json'
    else:
        raise ValueError('Invalid file type')

    # كتابة البيانات إلى الملف
    with open(file_name, 'w', newline='', encoding='utf-8') as file:  # تحديد الترميز كـ utf-8
        if file_type == 'csv':
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for product in products:
                #لإضافة الأعمدة وفق صف المنتجات بالترتيب الذي أريده
                writer.writerow({'name': product.name, 'price': product.price, 'description': product.description, 'specifications': product.specifications, 'rating': product.rating})
        elif file_type == 'json':
            data = [{'name': product.name, 'price': product.price, 'description': product.description, 'specifications': product.specifications, 'rating': product.rating} for product in products]
            json.dump(data, file, indent=2, ensure_ascii=False)  # تعديل الترميز كـ utf-8

# تعريف الدالة الرئيسية
def main():
    products = []
    #إضافة الأجهزة إلى المصفوفة مع توصيفاتهم
    amazon(products)
    #إضافة الأجهزة إلى المصفوفة السابقة مع الأجهزة القديمة 

    laptopsy(products)
    #حفظ الأجهزة في ملف csv
    save_products(products, 'csv')
    #حفظ الأجهزة في ملف json

    save_products(products, 'json')

# تشغيل الدالة الرئيسية
if __name__ == '__main__':
    main()

