17wo
========================

### 依赖
- python3
- [requests](http://docs.python-requests.org)

### 使用
- 首先修改脚本，将 ```check = checkin("phonenum", "passwd")```  中phonenum，passwd修改成对应的登录17wo.cn的手机号码和服务密码

- ```python3 17wo.py checkin``` 签到

- ```python3 17wo.py redpocket``` 抽红包, 每执行一次抽一次红包，如有多次抽红包机会请相应执行多次

- ```python3 17wo.py gaintask```  领取登录和签到任务的成长值

- ```python3 17wo.py diamond``` 点亮流量钻石

- ```python3 17wo.py ``` 默认依次执行 checkin gaintask redpocket diamond




