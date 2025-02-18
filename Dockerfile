# Sử dụng Python 3.9 làm image cơ bản
FROM python:3.9

# Đặt thư mục làm việc trong container
WORKDIR /code

# Sao chép file requirements.txt vào container
COPY ./requirements.txt /code/requirements.txt

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . /code/

# Mở cổng 80 để truy cập API
EXPOSE 80

# Chạy ứng dụng FastAPI với Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
