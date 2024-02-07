# REST API 실습 - TodoList
### 참고한 블로그 
[Django 간단한 투두리스트 API -  1](https://djangojeng-e.github.io/2022/06/12/Django-간단한-투두리스트-API-1/)

## 0. 전체 디렉토리 구조

```python
.
├── db.sqlite3
├── manage.py
├── todo
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── todolist
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## 1. 프로젝트 생성 및 앱 등록

### 가상환경 구성 후 프로젝트 및 앱 생성

```python
virtualenv venv # 가상환경 구성
venv/Script/activate # 가상환경 실행
activate.bat # 위 키워드가 안 먹으면 Script 폴더까지 간 후 이 파일 실행 
pip install django # 가상환경 실행 후 장고 설치 
django-admin startproject todo . # 장고 프로젝트 생성
python manage.py startapp todolist # todolist라는 앱 생성
# 여기까지 했을 때 루트 폴더 안에 todo, todolist, manage.py 존재 
```

### 프로젝트에 앱 연결

`todo/settings.py` 의 `INSTALLED_APPS` 에 `‘todolist’`  추가

## 2. 모델 작성

- 일반적인 흐름은 앱에 모델 작성(models.py) → url 구조 작성(urls.py) → view 작성(views.py) → 페이지별 html 템플릿 작성
- api 확인만 하기 위해 과정 간소화

### 데이터베이스 모델 작성

`todolist/models.py` 

```python
from django.db import models
from django.contrib.auth.models import User 	
# Django 기본 User 모델을 가져옴 

# Create your models here.

class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

### 모델 적용

```python
python manage.py makemigrations 
python manage.py migrate
python manage.py runserver # 서버 실행 
```

## 3. 관리자 유저(Superuser) 생성

```python
python manage.py createsuperuser
```

이후 http://127.0.0.1:8000/admin으로 접속하여 생성한 관리자 계정으로 로그인

## 4. admin에 작성한 모델 추가

`todolist/admin.py` 

```
from django.contrib import admin
from .models import TodoList
admin.site.register(TodoList)
```

### 모델 데이터 생성

**1) shell에서 데이터 추가**

```python
python manage.py shell
from todolist.models import TodoList
from django.contrib.auth.models import User
user = User.objects.get(id=1) # 관리자는 첫번째 사용자 - id가 1, <User: todolist> 객체
TodoList.objects.create(user=user, title="Django API 학습하기", content="간단한 예제를 통해 API를 학습해보자") # <TodoList: Django API 학습하기> 객체 생성
TodoList.objects.all() # 생성된 데이터 조회 - <QuerySet [<TodoList: Django API 학습하기>]>
```

**2) admin에서 추가** 

- admin 페이지에 레코드를 생성할 모델을 선택하고 input form에 작성 후 save

**3) Django-seed를 이용해 데이터 채우기**

- `pip install django-seed` (루트 폴더에 설치)
- 프로젝트 폴더 `settings.py` 의 `INSTALLED_APPS` 에 `‘django_seed’`  추가
- `python manage.py seed <앱이름> --number=<생성 데이터 갯수>`

**현재 Django 버전 5에서 django-seed를 사용할 때 발생하는 문제**

1. `psycopg2` 를 찾을 수 없음 - 라이브러리를 pip install로 설치하면 해결 
2. is_dst를 timezone.make_aware로 전달하면 인식하지 못함 (deprecate - 더 이상 사용하지 않다) 
    
    https://github.com/Brobin/django-seed/issues/119
    

## 5. Django REST Framework 설치

- `pip install djangorestframework`
- `settings.py` 의 `INSTALLED_APPS` 에 `‘rest_framework’`  추가

### REST 개념

- Representational State Transfer (REST) 의 약자
- https://www.techtarget.com/searchapparchitecture/definition/REST-REpresentational-State-Transfer
    
    REST (REpresentational State Transfer) is an architectural style for developing web services. REST is popular due to its simiplicity and the fact that it builds upon existing systems and features of the internet’s HyperText Tyransfer Protocol (HTTP) in order to achieve its objectives.
    
- 2000년대에, Roy Fielding이 처음 제안한 구조로, API를 웹상에서 개발하는 방법론임. 즉, API가 HTTP 프로토콜 위에 개발되는 방식이 REST

### **REST의 주요 특성**

1. HTTP 처럼 무상태 (Stateless) 이다
2. 보편적인 HTTP verbs 를 지원한다 (예, GET, POST, PUT, DELETE)
3. 데이터를 `json` 형태나 `XML` 형태로 반환한다.

## 6. API 작성

### urls.py 세팅

`todo/urls.py` 

```
from django.contrib import admin
from django.urls import path, include # include 가져오기

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todolist.urls'))
    # todolist의 urls.py 를 포함시켜줌
]
```

`todolist/urls.py` 

```python
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('api/todolist',), 
    # api/ 다음에 오는 단어에 따라서 호출되는 API 뷰가 달라지게 url pattern을 	  작성할수 있다.
]
```

### todolist 조회 API 작성

1. todolist 앱 안에 `serializers.py`파일 생성 및 작성 (todolist/serializers.py)
    - `serializer` 는 queryset 이나 모델 인스턴스 같은 복잡한 데이터들을 인터넷 상에서 쉽게 사용될 수 있는 포맷으로 변환해 준다. 보통 json 형태로 전환
    
    ```python
    from .models import TodoList 
    from rest_framework import serializers 
    
    class TodoSerializer(serializers.ModelSerializer):
        class Meta:
            model = TodoList 
            fields = ("user", "title", "content", "dt_created")
    ```
    
2. `views.py` 파일에 `TodoListAPIView` 클래스 작성
    - `rest_framework`에서 `generics` 를 가져오면, generic 클래스로 쉽게 API 를 구현할 수 있음
    
    ```python
    from django.shortcuts import render
    
    from .models import TodoList 
    from rest_framework import generics 
    # serializers.py 파일에서 정의한 TodoSerializer를 가져옴
    from .serializers import TodoSerializer  
    
    class TodoListAPIView(generics.ListAPIView):
        queryset = TodoList.objects.all() 
        serializer_class = TodoSerializer
    ```
    
3. `urls.py` 파일에 url 정의 및 `TodoListAPIView` 를 호출하도록 코드 작성
    
    ```python
    urlpatterns = [
        path('api/todolist/', TodoListAPIView.as_view(), name="todo-list"),
    ]
    ```
    
4. 브라우저로 테스트
    - 서버 구동 후 http://127.0.0.1:8000/api/todolist/ 접속
