# 网络空间检索平台对比

最近网络空间检索平台雨后春笋般涌现，本篇文章以一个使用者的视角来做一下对比

## 语法

目前网络上比较知名的网络空间检索平台有白帽汇的 [fofa](https://fofa.so/)、360的 [quake](https://fofa.so/)、知道创宇的 [zoomeye](https://www.zoomeye.org/)、安恒的 [sumap](https://sumap.dbappsecurity.com.cn/)、奇安信的 [hunter](https://hunter.qianxin.com/)、以及国外的 [shodan](https://www.shodan.io/)

简单对比下语法上的差异，当然，不一定准确，也不一定就是我下面列出的字段名称，各家对于字段名称可能有些差异

### 公共

首先是大家都共有的字段搜索，

| 字段名称      | 字段说明                     |
|---------------|------------------------------|
| title         | 网站标题                     |
| body          | 正文，或者说响应体           |
| cert          | 证书内容                     |
| ip            | ip或ip段                     |
| port          | 端口                         |
| protocol      | 协议                         |
| server        | http headers里面的Server字段 |
| base_protocol | 传输层协议                   |
| os            | 系统                         |
| asn           | 自治域号码                   |
| status_code   | web状态码                    |
| icon_hash     | 图标hash                     |
| region        | 地区                         |
| app           | 应用指纹                     |

### 时间

shodan 并没有针对采集时间的 before 和 after 语法，国内各家貌似都有针对采集时间的查询

### 域名

shodan 并没有针对ip关联的域名做语法，国内各家貌似都有针对域名的查询

### ipv6

根据几家的说明文档来看，除了hunter，其他家都有提供ipv6的资产查询，不过现阶段用得较少

### hostname

除了 sumap 和 hunter，其他家都有提供对于rDNS的查询（即hostname字段），不过该功能也用得少

### 证书细化

证书内容其实就是一个文本内容，各家在针对这个文本的解析上有多有少，目前看起来在这一块shadon和quake是做得最细致的

#### fofa

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/787cafd29b3e71995247b0e67e17a662.png)

#### quake

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/19e2e341c91b39830c0fa2dbc745f0f7.png)

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/96337f0224e29dbe83daaab0ca3ad9d0.png)


#### shodan

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/c58eca20aaa6e06922529dd8032a3b42.png)

#### zoomeye

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/4be1bdd5aa260b441b982508960edfd9.png)

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/64cdf8c008ca3bc6c689815fab35e870.png)


#### sumap

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/467c17b8c29e79c4c3adb185ce4c7377.png)

#### hunter

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/05793aa10c36e8282f1523c3f4afd457.png)

大家要是想自己在命令行解析推荐一个工具 [cfssl-certinfo](https://github.com/cloudflare/cfssl)，大概可以解析出的内容如下

```shell
cfssl-certinfo -cert kubernetes.pem
{
  "subject": {
    "common_name": "kubernetes",
    "country": "CN",
    "organization": "k8s",
    "organizational_unit": "System",
    "locality": "BeiJing",
    "province": "BeiJing",
    "names": [
      "CN",
      "BeiJing",
      "BeiJing",
      "k8s",
      "System",
      "kubernetes"
    ]
  },
  "issuer": {
    "common_name": "kubernetes",
    "country": "CN",
    "organization": "k8s",
    "organizational_unit": "System",
    "locality": "BeiJing",
    "province": "BeiJing",
    "names": [
      "CN",
      "BeiJing",
      "BeiJing",
      "k8s",
      "System",
      "kubernetes"
    ]
  },
  "serial_number": "243750511260095960201836502027625859126538784827",
  "sans": [
    "",
    "",
    "kubernetes",
    "kubernetes.default",
    "kubernetes.default.svc",
    "kubernetes.default.svc.cluster",
    "kubernetes.default.svc.cluster.local",
    "127.0.0.1"
  ],
  "not_before": "2017-12-23T10:27:00Z",
  "not_after": "2018-12-23T10:27:00Z",
  "sigalg": "SHA256WithRSA",
  "authority_key_id": "6E:45:FB:5F:1F:73:87:3E:C3:C:54:AB:74:95:2A:FB:44:E0:9B:D8",
  "subject_key_id": "62:EA:5A:DC:13:C4:5F:D5:EC:DB:13:77:DA:E1:90:1F:C9:4B:10:14",
  "pem": "-----BEGIN CERTIFICATE-----\nMIIEcTCCA1mgAwIBAgIUKrImpH2fsSHYOsDcp3FzPmYT0DswDQYJKoZIhvcNAQEL\nBQAwZTELMAkGA1UEBhMCQ04xEDAOBgNVBAgTB0JlaUppbmcxEDAOBgNVBAcTB0Jl\naUppbmcxDDAKBgNVBAoTA2s4czEPMA0GA1UECxMGU3lzdGVtMRMwEQYDVQQDEwpr\ndWJlcm5ldGVzMB4XDTE3MTIyMzEwMjcwMFoXDTE4MTIyMzEwMjcwMFowZTELMAkG\nA1UEBhMCQ04xEDAOBgNVBAgTB0JlaUppbmcxEDAOBgNVBAcTB0JlaUppbmcxDDAK\nBgNVBAoTA2s4czEPMA0GA1UECxMGU3lzdGVtMRMwEQYDVQQDEwprdWJlcm5ldGVz\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAp9OWY14XEX7WtXMVKqrq\naWdIw/EQgwNNmQmI7LcnEmggK5XTv84/mhzEiDGtz9LZ0Xw5IPVP2emPKOJE0N9p\nKRAV2sMS1U7FJKOIuasKk2sa5QstWhNPjDdS+jNSvaFvT3MAWg50LfD6/wWAnSiV\n4r9kA9ff+d8QhgavZvSX19KCkerP0Yjjn2ujD6kNtHOanFcA8i74UF8oM3qHOo1T\nFglHx+ZD0D6BV5aCQdTyWo9QwBExPC6AGbUydAIewxwCefPz0IalPXvZo9AS05dt\nEX6cTvP+hC3RQxBfp0EVHD/UPV/n+YDspx0/oYexMrFn2MFVkTXLp64QUc0Z7MQe\nGwIDAQABo4IBFzCCARMwDgYDVR0PAQH/BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUF\nBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBRi6lrcE8Rf1ezb\nE3fa4ZAfyUsQFDAfBgNVHSMEGDAWgBRuRftfH3OHPsMMVKt0lSr7ROCb2DCBkwYD\nVR0RBIGLMIGIggCCAIIKa3ViZXJuZXRlc4ISa3ViZXJuZXRlcy5kZWZhdWx0ghZr\ndWJlcm5ldGVzLmRlZmF1bHQuc3Zjgh5rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNs\ndXN0ZXKCJGt1YmVybmV0ZXMuZGVmYXVsdC5zdmMuY2x1c3Rlci5sb2NhbIcEfwAA\nATANBgkqhkiG9w0BAQsFAAOCAQEALL0sJDq2dGGN8leHcUc2+Sgy9MIQPzXSNhug\nPJaamIpZBwAvP6yD/fEACapNciY4iMleoy/f8L98BzlVHTDchxV8TwGfX3TgeAlq\n8C6/qagmhgFDi0mjv3cnoLp3mj3mFE47UuQ1L4uIZEztbZfPjCGdpRyA/4Dw1RjQ\nDB41hGBVTQ4sbFbTNtQMYz5lxD23I7UuXyBeQ2WFLYdMtuld01iQ1vu0Hh0jYvie\nYyKtlbrpnvOIFvTx2qLB78Qv0427QjxjjyC5bJqQZS42T7X4ynXiaQ8OB5mMAVP/\nzKCnlTMlt+d4M7wv+CU6/klPVQasF8D52Ykvu8mPEHshelk/CA==\n-----END CERTIFICATE-----\n"
}
```

### 漏洞

支持对暴露漏洞进行搜索的貌似只有 shodan 和 sumap

### 网站备案

国内除了 zoomeye，基本都有对备案有简单的支持

可以对备案号进行搜索，当然，sumap更加细化了该功能

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/0900d0beb6803200df0362d5ae8b1767.png)

而 hunter 则是扩展了该功能，做了更多关联工作

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/61a86d9d7645253456ea5164223eeb05.png)

### 应用协议细化

比较了几家来看的话，做的最好的是quake，针对协议方面做了很多细化，其他各家基本只是针对http做了细化（比如header，header中的server字段，web图标，http正文等等），shodan也做了一些协议的细致化提取，但是没有quake多

quake不仅对http做了细化，还对ftp、rsync、ssh、upnp、snmp、docker、dns、elastic、hive、mongodb、ethernetip、modbus、s7、smb等做了细致化的内容提取，其中rsync和mongo还做了是否未授权的指纹提取

RDP截图，这个功能我也不知道在什么场景能用到，目前来看支持的有fofa、quake、shodan、sumap，其他家不支持，其中quake还对截图进行了ocr文字提取

### 附加语法

上面提到了一些我们搜索常见常用的语法，下面来说一下各家一些特色的东西

#### fofa

fofa中有个功能是 `fid`，能够针对网站生成唯一的特征id；通过对相同的fid进行聚合，来实现用户的查询需求；最终解决未知资产发现、自动聚类网站、资产指纹扩充等需求），常见需求：通过同一套业务系统定位到所有使用这套系统的网站

fofa还针对web网页中的js做了处理 `js_name` 和 `js_md5`，可以针对js做一些搜索，可以想到的场景比如某个供应链公司的几套产品，会用自己内部的某个公有js，那么可以通过该js聚类出来

fofa里面还有 `is_fraud` 和 `is_honeypot`，`is_fraud` 用来排除仿冒/欺诈数据，`is_honeypot`用来
排除蜜罐数据，对于一些hvv场景下的红队攻击比较有用

#### quake

quake对于应用识别也做了一些归类，可以根据应用属于什么类别，或者属于那一层，以及生产厂家等等来做查询，具体可以查看下图

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/c352246a7eb1e503fabc23df1819c628.png)

quake对ip的运营商和单位做了一些归类，可以查看IP归属的运营商和单位，查询ip单位这个功能如果做得准确的话会大大方便红队

#### shodan

shodan对一些云服务做了额外识别

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/235b1be6f1c025962e7e91265ee1b5f7.png)

#### zoomeye

zoomeye提供了一个 `dig` 查询，但是我确实不清楚这个是干嘛的，看起来像是跟踪路由解析的每一跳，但我测试了以下，就 `baidu.com` 和 `google.com` 结果多点，其他的域名基本查不到，本人暂不清楚这个过滤语法的功能和目的

#### sumap

除了上面提到的漏洞和备案，sumap对于一些网站做了内容识别然后分了类，但是并未提供更多选项和样例，针对一些政府打击非法网站可能会比较有用

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/5a8395ca06dbbb7e7dc20c81607fc870.png)


#### hunter

hunter比较特别的功能就是备案了，上面也有提到，hunter有根据网页的备案号将资产和备案信息关联起来，可以通过备案信息来搜索资产，这个功能对于国内红队和hvv场景比较有用，或者做一些行业资产评估

## 界面和功能

为什么把功能单独拆出来呢，因为有些东西可能并没有以语法形式提供，但是在页面上能看到，所以我把它归到了界面功能上

首先是聚合分析，这是每一家都有的，下面说一下各家的特色功能

### shodan

shodan提供了给定资产扫描的功能

### zoomeye

zoomeye可以针对特定语法进行订阅，然后它会提供一个周期内的资产变化

zoomeye提供了恶意ip标记功能

### quake

quake针对相似的网站图标做了聚合

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/3ee7f34cb7501a4dd5b3fc6e248afe73.png)

quake也可以像fofa一样排除蜜罐，不过是在页面上提供的，也可以排除cdn

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/4fe68989e952dc1006996f09a41a22e2.png)

### sumap

sumap提供了三个不同于其他家的聚合功能，分别是whois聚合分析，dns解析聚合分析，以及根据根资产做的暴露面分析

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/b653b8ff174fccd9409af44554d8c5e7.png)

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/7d9e9dd2e4b528593a6d128de02f1b33.png)

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/7612defb01d2cdc8526e821033277df8.png)

同时sumap提供了一个漏洞收集页面，可以直接点选漏洞进行产品梳理，这个比shodan要方便

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/39565674fbbf64249d68c57f306a4590.png)

同时对漏洞做了一些聚合，这里就不截图了

### hunter

hunter做了一个比较人性化的设计，就是语法关键词提示，输入 `p`，就会出现一个语法推荐，出现所有包含 `p` 的语法关键词，类似于ide里面的只能提示，下面接着的就是大家都有的指纹提示了

做得还有个比较人性化的一点是，自动帮你选了想要的状态码和资产类别

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/3a9970a514c6714d23304d30781014a5.png)

此外对于登录页有额外的标签提示

![](https://raw.githubusercontent.com/akkuman/pic/master/img/2021/10/4c40ac70a67c82671b273ce038b92221.png)

hunter针对各家的搜索语法都有一定的兼容性

## 数据更新周期

- shodan更新周期为一周（来源: https://help.shodan.io/the-basics/on-demand-scanning）
- hunter 7天更新国内资产；30天更新海外资产（来源: https://hunter.qianxin.com/home/helpCenter）

其他家的未见到说明


## 收费体系

综合来看，对于重度使用者（指那些需要使用api自动化的人），fofa是最实惠的，买断制，只对单次导出数量有限制，对导出总量没有限制。

其他家各种收费体系，基本都是每月给你一定量的免费查询额（按照每条或者每页），付费可以增加查询额，总体上来说就是对于每月查询总量做了限制

## 个人总结

因为工作上偶尔接触红队，所以会更偏向于国内资产的探测，所以以下的均是国内的网络空间检索网站

目前来看，hunter除了体验上的优化外，比较吸引人的是备案关联信息的查询，这个对于国内的一些应用场景很适用

quake的资产分类做得是这些中做得最好的

关于漏洞搜索，sumap比较合适

如果想要资产监控，可能zoomeye更合适（或者是账号等级的原因，其他平台未见到）


## 参考资料

- [证书各个字段的含义](https://www.cnblogs.com/iiiiher/p/8085698.html)
- [fofa.so](https://fofa.so/)
- [quake帮助文档](https://quake.360.cn/quake/#/help?id=5eb238f110d2e850d5c6aec8&title=%E6%A3%80%E7%B4%A2%E5%85%B3%E9%94%AE%E8%AF%8D)
- [shodan Filter Reference](https://beta.shodan.io/search/filters)
- [zoomeye用户手册](https://www.zoomeye.org/doc?channel=user)
- [sumap](https://sumap.dbappsecurity.com.cn/)
- [hunter 基础语法介绍](https://hunter.qianxin.com/home/helpCenter)
- [Feature引擎正式上线！“拓线”功能开放！](https://nosec.org/home/detail/4824.html)
