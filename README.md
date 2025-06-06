# Hướng Dẫn Cài Đặt và Chạy Backend FastAPI

url: https://be-maynenkhi.onrender.com/docs

1. **Cài đặt môi trường ảo env**:

```bash
pip install virtualenv 
```

2. **tạo môi trường ảo với name myenv**:

```bash
python -m venv myenv
```

3. **start môi trường ảo myenv**:

```bash
myenv\Scripts\activate
```

4. **Cài đặt các phụ thuộc**:

```bash
pip install -r requirements.txt
```

5. **Chạy ứng dụng**:

```bash
python main.py
```

6. **Biến môi trường**:

| Tên biến môi trường      | Giá trị               | Mô tả                               |
| ------------------------ | --------------------- | ----------------------------------- |
| PORT        | 6879 | port mà ứng dụng chạy |
| BASE_URL    | mongodb://localhost:27017/ | Url mongodb                     |
| CLOUD_NAME | __________| cloud name cloudinary |
| API_KEY | hhdffgfh | API key cloudinary |
| API_SECRET | hhdheher | API SECRET cloudinary |
