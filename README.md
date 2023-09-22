# WebFrameworkTest
> web框架简单压测

## 压测工具：wrk
mac 安装
```bash
brew install wrk
```
window安装可能要依赖它的子系统才方便安装，或者换成其他的压测工具例如JMeter。

## 压测的web框架
框架      | 介绍                | 压测版本    | 官网/Github                               |
| ------- | ----------------- | ------- | --------------------------------------- |
| FastAPI | 基于Python的高性能web框架 | 0.103.1 | https://fastapi.tiangolo.com/          |
| Sanic   | Python的异步web服务器框架 | 23.6.0  | https://sanic.dev/zh/                  |
| Tornado | Python的非阻塞式web框架  |    6.3.3     | https://www.tornadoweb.org/en/stable/ |
| Gin     | Go语言的web框架        |   1.9.1      | https://gin-gonic.com/                 |
|         |                   |         |                                         |
| Fiber   | todo              | todo    | todo                                    |
| Flask   | todo              | todo    | todo                                    |
| Django  | todo              | todo    | todo


## 快速使用
clone 项目
```git
git clone https://github.com/HuiDBK/WebFrameworkPressureTest
```

python 框架的依赖安装
```python
cd python_web

pip install -r requirements.txt
```

go 框架的依赖安装
```go
cd go_web

go mod tidy
```

## 压测结果
web框架   | 压测类型    | 测试时长 | 线程数 | 连接数 | 请求总数                | QPS                   | 平均延迟    | 最大延迟      | 总流量      | 吞吐量/s   |
| ------- | ------- | ---- | --- | --- | ------------------- | --------------------- | ------- | --------- | -------- | ------- |
| FastAPI | 普通请求    | 30s  | 20  | 500 | **2298746（229w）**   | **76357.51（76k）**     | 3.06ms  | 36.65ms   | 383.64MB | 12.74MB |
|         | MySQL查询 | 30s  | 20  | 500 | **180255****(18w)** | **5989.59****(5.9k)** | 38.81ms | 226.42ms  | 36.95MB  | 1.23MB  |
|         | Redis缓存 | 30s  | 20  | 500 | **730083****(73w)** | **24257.09****(24k)** | 9.60ms  | 126.63ms  | 149.70MB | 4.97MB  |
|         |         |      |     |     |                     |                       |         |           |          |         |
| Sanic   | 普通请求    | 30s  | 20  | 500 | **3651099（365w）**   | **121286.47（120k）**   | 1.93ms  | 61.89ms   | 497.92MB | 16.54MB |
|         | MySQL查询 | 30s  | 20  | 500 | **198925（19w）**     | **6609.65（6k）**       | 35.22ms | 264.37ms  | 34.72MB  | 1.15MB  |
|         | Redis缓存 | 30s  | 20  | 500 | **1022884（100w）**   | **33997.96（33k）**     | 6.91ms  | 217.47ms  | 178.52MB | 5.93MB  |
|         |         |      |     |     |                     |                       |         |           |          |         |
| Tornado | 普通请求    | 30s  | 20  | 500 | **1068205（106w）**   | **35525.38（35k）**     | 6.54ms  | 34.75ms   | 280.15MB | 9.32MB  |
|         | MySQL查询 | 30s  | 20  | 500 | **169471（16w）**     | **5631.76（5.6k）**     | 41.29ms | 250.81ms  | 51.88MB  | 1.72MB  |
|         | Redis缓存 | 30s  | 20  | 500 | **599840（59w）**     | **19947.28（19k）**     | 11.69ms | 125.75ms  | 183.63MB | 6.11MB  |
|         |         |      |     |     |                     |                       |         |           |          |         |
| Gin     | 普通请求    | 30s  | 20  | 500 | **3787808（378w）**   | **125855.41（125k）**   | 2.45ms  | 186.48ms  | 592.42MB | 19.68MB |
|         | MySQL查询 | 30s  | 20  | 500 | **308836（30w）**     | **10260.63（10k）**     | 40.89ms | **1.12s** | 61.26MB  | 2.04MB  |
|         | Redis缓存 | 30s  | 20  | 500 | **972272（97w）**     | **32305.30（32k）**     | 7.18ms  | 79.40ms   | 193.79MB | 6.44MB

    
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/315fc0d3a36d4c75b7435f0c3291c903~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1000&h=600&s=49821&e=png&b=ffffff)


![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7ce2cc90cd934084a90cbfe36090c48b~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1000&h=600&s=43692&e=png&b=ffffff)


![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7a54aa632e004249a6cf4816f096200b~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1000&h=600&s=42793&e=png&b=ffffff)