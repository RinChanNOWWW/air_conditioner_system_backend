# Air Conditioner System Web Backend

## 准备工作

- 安装 Django：

```bash
pip3 install Django
```

官网：https://www.djangoproject.com/

- 安装 Django REST framework：

```bash
pip3 install djangorestframework
```

官网：https://www.django-rest-framework.org

- 将源代码克隆到本地：

```bash
git clone KagamineRinSuki/air_conditioner_system_backend
```

## 初始化数据库

1. 进入项目目录：

```bash
cd air_conditioner_system_backend
```

2. 生成数据表：

```bash
python3 manage.py makemigrations
python3 manage.py migrate       
```

## 启动服务器

```bash
python3 manage.py runserver 
```

## 可视化 API 

具体调用方法见组内 API 文档。
