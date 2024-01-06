# 📺생활코딩(OpenTutorials) Python Django Web Framework
### 📺[Lecture Link](https://www.youtube.com/playlist?list=PLuHgQVnccGMDLp4GH-rgQhVKqqZawlNwG)
<br/>

## 📃목차
|No.|Title|No.|Title|
|:---|:---|:---|:---|
|1|[수업 소개](#수업-소개)|8|[읽기 기능 상세 보기 페이지 구현](#읽기-기능-상세-보기-페이지-구현)|
|2|[설치](#설치)|9|[생성 기능 구현 (form)](#생성-기능-구현)|
|3|[포트의 개념](#포트의-개념)|10|[생성 기능 (method=GET, POST)](#생성-기능-(method=get,-post))|
|4|[app 만들기](#app-만들기)|11|[생성 기능 (request response object)](#생성-기능-(request-response-object))|
|5|[Routing URLConf](#Routing-URLConf)|12|[DELETE](#delete)|
|6|[Django를 쓰는 이유](#Django를-쓰는-이유)|13|[수정 기능](#수정-기능)|
|7|[홈페이지 읽기 기능 구현](#홈페이지-읽기-기능-구현)|14|[수업을 마치며](#수업을-마치며)|

<br/>

## 🔖내용 정리
## 1. 수업 소개
- 효율적인 수정을 위한 방법
- 웹 페이지를 만들 때 공통적으로 해야 하는 작업을 모아둔 것이 웹 프레임워크
    - JSP, Servlet, Spring
    - Laravel, Codeignitor
    - Ruby on rails
    - Express.js
    - Flask, FastAPI
    - Django
- 사용자의 요청이 들어올 때마다 순간적으로 새 웹 페이지를 찍어 보여주는 장고

## 2. 설치
### 설치 및 프로젝트 생성 커맨드

```
pip install django
django-admin startproject myproject . 
```
### 프로젝트 구성
- settings.py
    - 프로젝트 운영에 필요한 설정들
- urls.py
    - 사용자가 접속하는 path에 따라 요청을 어떻게 처리할 것인가 (라우팅)
- manage.py
    - 프로젝트를 진행하는 데 있어 필요한 여러 기능이 들어간 유틸리티 파일
### 프로젝트 실행
```
python manage.py runserver
python manage.py runserver 8888
```
- Ctrl + C로 서버 종료
- 8000번 포트가 이미 사용중인 경우 명령 뒤에 다른 포트번호 작성

## 3. 포트의 개념
- 두 대의 컴퓨터(서버와 클라이언트)
    - 서버 컴퓨터에는 3개의 서버 sw가 동작중
    - 클라이언트 컴퓨터에서 서버에 접속할 때 누구와 통신할지 결정하기 위해 port 개념 등장
    - 주소에 포트 번호를 적으면 그 포트에서 listening하고 있는 서버와 연결
    - 파이썬 서버는 기본적으로 8000번 포트에서 listening
<img width="991" alt="Untitled (21)" src="https://github.com/hanby-choi/BackendStudy/assets/76518934/8d803853-de94-4aa3-8c5b-24458192d52e">

## 4. app 만들기
### app, view, function, model
<img width="1163" alt="Untitled (22)" src="https://github.com/hanby-choi/BackendStudy/assets/76518934/c2153984-3ba9-4aae-8dfe-2c7f84ace416">

- myproject 폴더 안에 프로젝트 설정이 들어감
- app이라는 더 작은 단위를 만들어 그 안에서 실제로 구현하는 것
- 연관된 로직들을 모아 그룹핑하고 싶을 때 정리정돈
- app 안에는 view가 들어가고 그 안에는 여러 함수가 들어감
- 사용자가 각각의 경로로 들어올 때 누구에게 위임할지 urls.py에 작성
- 앱 안의 urls.py에 작성한 내용에 따라 적당한 view, function에 위임
- 많은 경우 데이터베이스 사용 - 직접 접속하지 않고 model을 통해 DB를 사용
- DB에 있는 정보를 받아 클라이언트에 응답 - 최종적으로 html, json, xml 등의 데이터를 만들어 사용자에게 보내줌

## 5. Routing URLConf
### 라우팅 이론
<img width="1121" alt="Untitled (23)" src="https://github.com/hanby-choi/BackendStudy/assets/76518934/e89758a1-42c3-4b6a-a7f3-ddc9be4860e7">

- 뭘 만들든 라우팅부터 하게 됨
- 라우팅: 사용자가 접속한 각각의 경로를 누가 처리할지 지정하는 것
- 프로젝트 안에 있는 urls.py가 가장 큰 틀의 라우팅 수행 - 이것을 적당한 app에 위임하면 app이 view 안의 특정 함수로 위임

### 라우팅 실습
- urlpatterns에 라우팅과 관련된 내용을 정의해두어야 함
- `admin/`: 장고가 기본적으로 갖고 있는 관리자 화면으로 이동하기 위한 라우팅

```
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
```


<img width="1114" alt="Untitled (24)" src="https://github.com/hanby-choi/BackendStudy/assets/76518934/d55a16fd-284d-4179-8386-647d75daad18">

- myproject
```python
# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('myapp.urls'))
]
```

- myapp

```python
# urls.py
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('read/<id>/', views.read)
]

# views.py
from django.shortcuts import render, HttpResponse

def index(request):
    return HttpResponse('Welcome!')

def create(request):
    return HttpResponse('Create!')

def read(request, id):
    return HttpResponse('Read!' + id)
```

### app 만들기 실습

## 6. Django를 쓰는 이유 
### 웹 서버와 웹 애플리케이션 서버의 차이
- 웹 서버
    - apache, nginx, IIS
    - 필요한 웹 페이지를 미리 만들어두어야 함
    - 미리 준비된 페이지로 접속
    - 정적 (static)
    - 성능이 굉장히 빠름 (이미 준비된 걸 쓰니까)
- 웹 애플리케이션
    - django, flask, php, jsp, ROL
    - 웹 페이지 생성 공장 프로그램 하나만 만들어두면 됨
    - 1번에 해당되는 데이터를 DB에서 가져와서 그 순간에 html 코드를 만들고 응답
    - 동적 (dynamic)
    - 웹 서버에 비해 굉장히 느리지만 신경 쓰일 정도의 차이는 아님
    - 유지 보수가 훨씬 쉬움
    - 개인화된 정보를 만들어줄 수 있음

### 동적 사례 실습
- welcome 대신 랜덤 숫자 띄우기 (random 모듈)
- 출력 위해 문자열로 형변환 필요

## 7. 홈페이지 읽기 기능 구현
### Read
- 홈페이지/상세 보기 구성
- 파이썬에서 문자열 사이에 변수를 넣고 싶다면 문자열 앞에 f를 붙이고 문자열 사이 변수 넣을 곳에 중괄호 {} 작성

```python
from django.shortcuts import render, HttpResponse

topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is...'},
    {'id': 2, 'title': 'view', 'body': 'View is...'},
    {'id': 3, 'title': 'model', 'body': 'Model is...'}
]

def index(request):
    global topics 
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return HttpResponse(f'''
    <html>
        <body>
            <h1>Django</h1>
            <ol>
                {ol}
            </ol>
            <h2>Welcome</h2>
            Hello, Django
        </body>
    </html>
    ''')

def create(request):
    return HttpResponse('Create!')

def read(request, id):
    return HttpResponse('Read!' + id)
```

## 8. 읽기 기능 상세 보기 페이지 구현
- 코드의 부품화
- 유지보수에 용이
- index에 있던 내용을 HTMLTemplate 함수로 분리하되 본문 내용만 article로 분리 → index(), read()에서 본문 내용이 될 article 작성

```python
from django.shortcuts import render, HttpResponse

topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is...'},
    {'id': 2, 'title': 'view', 'body': 'View is...'},
    {'id': 3, 'title': 'model', 'body': 'Model is...'}
]

def HTMLTemplate(articleTag):
    global topics 
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ol>
                {ol}
            </ol>
            {articleTag}
        </body>
    </html>
    '''

def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

def create(request):
    return HttpResponse('Create!')

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article))
```

## 9. 생성 기능 구현 (form)
- 우클릭-검사(개발자 도구)-Network 탭

```python
from django.shortcuts import render, HttpResponse

topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is...'},
    {'id': 2, 'title': 'view', 'body': 'View is...'},
    {'id': 3, 'title': 'model', 'body': 'Model is...'}
]

def HTMLTemplate(articleTag):
    global topics 
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ul>
                {ol}
            </ul>
            {articleTag}
            <ul>
                <li><a href="/create/">create</a></li>
            </ul>
        </body>
    </html>
    '''

def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

def create(request):
    article = '''
        <form action="/create/">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit"></p>
        </form>
    '''
    return HttpResponse(HTMLTemplate(article))

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article))
```

## 10. 생성 기능 (method=GET, POST)
<img width="1826" alt="Untitled (25)" src="https://github.com/hanby-choi/BackendStudy/assets/76518934/12667440-c267-441c-a545-43edaf67fece">

- query string: 서버에 정보 전송할 때 사용
- 데이터를 브라우저가 서버로부터 요청하는 GET 방식
- 브라우저가 서버의 데이터를 변경할 때는 url에 쿼리스트링을 넣으면 절대 안됨 - 방문할 때마다 글이 늘어날 수도 있음
- POST 방식으로 보내면 url이 아니라 header 안에 데이터를 포함하여 눈에 보이지 않게 보낼 수 있음
- 403 에러 - CSRF verification failed 장고의 보안 기능

```python
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is...'},
    {'id': 2, 'title': 'view', 'body': 'View is...'},
    {'id': 3, 'title': 'model', 'body': 'Model is...'}
]

def HTMLTemplate(articleTag):
    global topics 
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ul>
                {ol}
            </ul>
            {articleTag}
            <ul>
                <li><a href="/create/">create</a></li>
            </ul>
        </body>
    </html>
    '''

@csrf_exempt
def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

def create(request):
    article = '''
        <form action="/create/" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit"></p>
        </form>
    '''
    return HttpResponse(HTMLTemplate(article))

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article))
```

## 11. 생성 기능 (request response object)
- HTTPRequest: 사용자의 요청과 관련된 여러 정보를 패키징해 객체 형태로 만들어 공급
- HTTPResponse 객체를 응답하면 장고에 의해 사용자의 브라우저로 전송됨

[Django](https://docs.djangoproject.com/en/5.0/ref/request-response/)

- HttpRequest.method
    - method 프로퍼티로 사용자의 요청 방식을 알 수 있음
- shortcut functions - redirect()

## 12. DELETE
- delete를 위한 페이지를 따로 만들면 GET 방식으로 해도 되겠지만 버튼 누르면 바로 서버 데이터 변경(수정) 작업 하고 싶음 → POST를 써야 함 (form)
- 삭제하려는 topic의 id와 일치하는 객체를 제외한 객체들을 for loop를 돌며 newTopics 배열에 저장한 후 topics를 newTopics로 교체하여 POST

## 13. 수정 기능
```python
@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title": topic['title'],
                    "body": topic['body']
                }
        article = f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="title" value={selectedTopic['title']}></p>
                <p><textarea name="body" placeholder="body">{selectedTopic['body']}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')
```

## 14. 수업을 마치며
- 현재 정보를 메모리에 보관 - 앱이 재실행될 때마다 리셋
    - 이를 막기 위해 데이터베이스 사용
- 장고의 Model - DB 사용이 쉬워짐
- script 태그를 이용한 공격 - 보안 문제
    <img width="1175" alt="Untitled (26)" src="https://github.com/hanby-choi/BackendStudy/assets/76518934/a6126ad0-7df5-4ffd-bf28-ab0bf190d6d2">

- 웹 애플리케이션은 결국 HTML 코드를 생성해주는 기계임
    - 파이썬 코드와 HTML 코드가 뒤섞여 가독성이 떨어짐
    - Template engine을 사용
    <img width="1753" alt="Untitled (27)" src="https://github.com/hanby-choi/BackendStudy/assets/76518934/623dce0c-9b0d-4c00-8cd5-b05c4b2e812e">
