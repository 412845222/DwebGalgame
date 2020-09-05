###安装指引
---
####前端 /dwebgalgame
这是一个正常的vuecli脚手架项目，安装方式

    cd /dwebgalgame
    npm install
    npm run server

PS:最新的vuecli4.0版本有 vue ui管理更方便，将项目导入vuecli管理比较好

---
####后端 /frameWebGame
这是一个Python语言环境下的Django项目，为了方便小伙伴搭建。
我没有删除 settings.py 这个文件，但如果你日后想要部署。建议自己重新用django建立一个project项目

    cd /frameWebGame
    python manage.py migrate
    python manage.py runserver 127.0.0.1:9000 #前端通信的api地址均接通到9000


---
感谢小伙伴们的支持，如果对这个小项目有任何意见，可以留言给我
个人博客：https://www.dweb.club
B站个人主页：https://space.bilibili.com/22690066
Python建站Q群：611516237
