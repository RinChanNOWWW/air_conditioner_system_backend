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

- 安装 django-cors-headers

```bash
pip3 install django-cors-headers
```

官网：https://www.django-rest-framework.org

- 将源代码克隆到本地：

```bash
git clone git@39.106.86.23:/home/git/air_conditioner_system_backend
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

## 一些要求

- 详单至少需要包含如下信息：房间号、开始送风时间、结束送风时间、送风时长、风速、费率、费用。账单至少包含如下信息：房间号、总费用、入住时间、离店时间。
- 统计报表的类型：日报、周报、月报、年报；缺省的报表以日报为准，主要查看酒店空调使用和消费的情况，主要展示每个房间的开关次数，使用空调的时长，总费用，被调度的次数、详单数、调温次数、调风次数；以某种格式展示出酒店所有房间的上述信息（列表或图形）。

## 成绩占比

- 考勤占10%  
- 小测占20% 
- 大作业占70%
    - 作业1：系统解决方案， 5%；      
    - 作业2：需求定义及领域模型， 10%；  
    - 作业3：用例模型， 20%； 
    - 作业4：设计模型-动态结构设计， 20%； 
    - 作业5：设计模型-静态结构设计， 5%； 
    - 作业6：系统验收， 40%