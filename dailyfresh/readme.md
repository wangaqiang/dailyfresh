学习完django框架后在b站找到的项目资源，感谢up主:'神奇的老黄',顺便复习git命令。
第一阶段：
	先是将数据库建立起来，然后跟着老师将django框架搭建起来，创建应用，注册应用，写注册功能，写register视图函数，最后将视图函数改成类。熟悉注册功能的流程如下，1.接受数据 2.进行数据校验 3.进行业务处理 4.使用celery进行发送激活邮件(需要加密用户的身份信息，生成激活token)
	深夜来袭，记录自己所踩的坑吧！
	1.Django中解决redis-py versions 3.2.0 or later. You have 2.10.6版本问题
	添加异步任务时报上述错误
	解决：从4.3.0到4.4.0的Kombu更新停止了对redis-py v2.10.6的支持，因此迫使我们升级redis-py版本。为了防止以后其他错误，这里我们只需降低kombu的版本即可
	pip3 install kombu==4.2.0
	pip3 install celery==4.1.1
	2.  File "/usr/local/lib/python3.5/dist-packages/kombu/transport/base.py", line 125, in __getattr__
    return self[key]
	原因：celery 版本过低
	解决：sudo pip3 install celery==4.1.1
	这两坑踩的我花费太多时间
第二阶段：
        先是登录功能的基本逻辑的学习，接着配置redis作为Django缓存和session存储后端，然后对父模版页进行抽取，对用户中心页面的显示。这几天因为刚开学事比较多，所以学的进度比较慢。也没有学太多的东西。遇到的问题抽取的时候忘记了加载staticfiles这行代码，导致报错。再无其他错误。接下来打算接着学习登录，完善登录的功能！
