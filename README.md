# License Plate Recognition
# Hướng dẫn sử dụng: 
## Clone git : 
```
 git clone https://github.com/taidao1901/LicensePlateRecognition.git
```
## Tạo Conda env bằng 2 cách:
 ### Cách 1:

 ```
    conda env create -f enviroment.yml 
 ```
 ###Cách 2:
  + B1: Khởi tạo môi trường
 ```
    conda create --name <tên env> python=3.9.12
    conda activate <tên env>
    pip install -r requirements.txt
 ```
### Khởi động server bằng lệnh
```
python manage.py runserver
```
