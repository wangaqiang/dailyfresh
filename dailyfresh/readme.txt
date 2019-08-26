学习完django框架后在b站找到的项目资源，感谢up主:'神奇的老黄',顺便复习git命令。
第一天：
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