import hashlib
import requests
import json
import base64
import datetime
import peewee
import logging
import sys
import argparse
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

class BreakLoop(Exception):
    pass

db = peewee.SqliteDatabase('db.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class IPData(BaseModel):
    uid = peewee.CharField(max_length=32, primary_key=True)
    ipport = peewee.CharField(max_length=25)
    protocol = peewee.CharField(max_length=30, null=True)
    web_title = peewee.TextField(null=True)
    domain = peewee.TextField(null=True)
    url = peewee.TextField(null=True)
    status_code = peewee.IntegerField(null=True)
    updated_at = peewee.DateField(null=True)
    company = peewee.TextField(null=True)
    icp_number = peewee.TextField(null=True)
    region = peewee.CharField(null=True)
    region_all = peewee.CharField(null=True)
    web_title_icon = peewee.BlobField(null=True)


now_time = datetime.datetime.now()


def get_md5(data: bytes) -> str:
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


class HunterApi:
    """奇安信Hunter Api
    
    Attributes:
        username: 用户名
        api_key: api-key，用户登录后在个人中心获取
    """
    def __init__(self, api_key, username='', interval=3):
        self.username = username
        self.api_key = api_key
        self.interval = int(interval)

    def getdata(
        self,
        rule: str,
        page: int,
        page_size: int,
        is_web: bool=True,
        status_codes: list=None,
        start_time: str=None,
        end_time: str=None,
    ):
        """从hunter爬取数据
        
        Args:
            rule: 搜索语法
            page: 页码
            page_size: 页大小
            is_web: 是否网站资产，默认为网站资产
            status_codes: 状态码列表，默认为200 
            start_time: 开始时间，格式为2021-01-01 00:00:00
            end_time: 结束时间，格式为2021-01-01 00:00:00  
        """
        status_codes = status_codes or [200,]
        status_codes = [str(i) for i in status_codes]
        status_code = ','.join(status_codes)
        search_rule = base64.urlsafe_b64encode(rule.encode())

        url = f'https://hunter.qianxin.com/openApi/search'
        params = {
            'api-key': self.api_key,
            'search': search_rule.decode(),
            'page': page,
            'page_size': page_size,
            'is_web': int(is_web),
            'status_code': status_code,
            'start_time': start_time,
            'end_time': end_time,
        }
        
        try:
            r = requests.get(url, params=params)
            return r.json()
        except Exception as e:
            logger.error(f'[!] 请求hunter接口出现问题: {str(e)}')
            return {}
    
    def crawler(
        self,
        rule: str,
        page_size: int=100,
        start_page: int=1,
        end_page: int=None,
        is_web: bool=True,
        status_codes: list=None,
        start_time: str=None,
        end_time: str=None,
    ):
        end_time = end_time or now_time.strftime("%Y-%m-%d %H:%M:%S")
        start_time = start_time or (now_time - datetime.timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
        page_index = start_page
        try:
            ip_count = 0
            while True:
                if end_page is not None and page_index > end_page:
                    break
                resp_data = self.getdata(rule, page_index, page_size, is_web, status_codes, start_time, end_time)
                # 处理非常规返回数据
                if resp_data.get('code') == 400 and '仅支持查询10000条数据' in resp_data.get('message', ''):
                    logger.ingo('[v]] [hunterApi] {rule} 爬取数据完成: 到10000条上限')
                    break
                elif resp_data.get('code') != 200:
                    logger.info(f'[!] [hunterApi] {rule} 爬取第 {page_index} 页时出错: {json.dumps(resp_data, ensure_ascii=False)}')
                    break
                # 处理ip数据
                ipdata_list = resp_data.get('data', {}).get('arr', [])
                if not ipdata_list:
                    logger.info(f'[v] [hunterApi] {rule} 爬取数据完成')
                    break
                # 对ip数据进行入库
                for ipdata in ipdata_list:
                    try:
                        # 异常数据不进行入库
                        if not (ipdata.get("ip") and ipdata.get('port')):
                            continue
                        web_title_icon = b''
                        try:
                            web_title_icon = base64.b64decode(ipdata.get('web_title_icon', ''))
                        except:
                            pass
                        ipport = f'{str(ipdata.get("ip", "")).strip()}:{str(ipdata.get("port", "")).strip()}'
                        uid = get_md5(f'{ipport}_{ipdata.get("domain")}_{ipdata.get("url")}'.encode('utf-8'))
                        ipdata_ = IPData(
                            uid = uid,
                            ipport = ipport,
                            protocol = ipdata.get('protocol'),
                            web_title = ipdata.get('web_title'),
                            domain = ipdata.get('domain'),
                            url = ipdata.get('url'),
                            status_code = ipdata.get('status_code'),
                            updated_at = ipdata.get('updated_at'),
                            company = ipdata.get('company'),
                            icp_number = ipdata.get('number'),
                            region = ipdata.get('city'),
                            region_all = f'{ipdata.get("country")}/{ipdata.get("province")}/{ipdata.get("city")}',
                            web_title_icon = web_title_icon,
                        )
                        ipdata_.save(force_insert=True)
                        ip_count += 1
                        logger.info(f'[*] 成功爬取第 {ip_count} 条数据: [{ipdata.get("url")}] [{ipdata.get("web_title")}] {ipport}')
                    except peewee.IntegrityError as e:
                        if 'unique' in str(e).lower():
                            # logger.info(f'[v] {rule} 在第 {page_index} 页出现了重复记录，爬取完成')
                            # raise BreakLoop()
                            logger.info(f'[v] {rule} 在第 {page_index} 页出现了重复记录')
                        else:
                            logger.error(f'[!] 保存数据到数据库出现异常: {str(e)}')
                    except peewee.PeeweeException as e:
                        logger.error(f'[!] 保存数据到数据库出现异常: {str(e)}')
                    except Exception as e:
                        logger.error(f'[!] 出现未知异常: {str(e)}')
                page_index += 1
                time.sleep(self.interval)
        except BreakLoop:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--apikey', type=str, help='hunter api key', required=True)
    parser.add_argument('--start_page', default=1, type=int, help='爬取开始页数', required=False)
    parser.add_argument('--end_page', default=None, type=int, help='爬取结束页数，默认为一直爬取，直至积分不够或者爬取完成', required=False)
    parser.add_argument('--page_size', default=100, type=int, help='每页爬取数量，最大为100', required=False)
    parser.add_argument('--rule', default='title="北京"', type=str, help='搜索语法', required=False)
    parser.add_argument('--is_web', default=1, type=int, choices=[0, 1], help="是否为网站资产", required=False)
    parser.add_argument('--interval', default=3.0, type=float, help="每次请求api之间的时间间隔", required=False)
    args = parser.parse_args()

    db.connect()
    db.create_tables([IPData,], safe=True)
    
    hunter = HunterApi(args.apikey, interval=args.interval)
    hunter.crawler(args.rule, args.page_size, args.start_page, args.end_page, bool(args.is_web))
