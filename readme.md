# 基于web的远程容器管理系统 
## 云计算课程考试 python docker
### 要求
现在有一台CentOS服务器，需要采用容器方式面向多租户提供web虚拟服务，
并为用户开发基于web的远程容器启停管理功能。每2人一组请按照以下具体任务实施：
（1）安装：安装最新版本的Docker，并开启远程管理接口。
（2）构造镜像：下载最新的httpd和mysql镜像；在httpd镜像基础上采用dockerfile构造自己的镜像myweb，
增加ssh远程登录服务和php引擎，使容器用户能够远程登录到自己的myweb容器内，开发基于php的web应用。
（3）基于myweb镜像建立一个管理web容器，在里面用php开发对docker的镜像和容器管理服务：
允许用户通过web界面实现镜像列表、活动容器列表、清除已停止容器、基于某个镜像创建容器、
停止容器、重亲启动容器、通过exec在运行中容器内执行命令。
（4）如果对python、Java等语言熟悉，可以用其它语言实现任务（3）。
完成上述实验和开发后，编写项目实施报告，并现场演示和报告。

评分标准：a
1、系统演示60分：经检查完成全部功能，得40分；创新功能加分0~5分；按照演示功能、答辩、
代码检查等，5组进行排序，得分从高到低为15、12、9、6、3分。
2、报告40分：根据条理清晰，思路正确，方案设计完备，总结到位等方面进行综合评分。