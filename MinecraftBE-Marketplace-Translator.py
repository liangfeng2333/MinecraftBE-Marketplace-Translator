# coding=utf-8
import re
import time
import hashlib
import http.client
import json
import os
import random
import urllib
import uuid
import requests
import shutil
import zipfile
# import json5
from pygtrans import Translate
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

if not os.path.exists('temp'):
    os.mkdir('temp')
sleep_time = 0.5
start = 0.0
encode_n = ['☹', '♢ⓝ', '\n']
config = '{\n    "GOOGLEAPI": {      /*谷歌翻译，使用pygtrans模块：https://github.com/foyoux/pygtrans   */\n        "target": "zh-CN",      /*目标语言，参照：https://pygtrans.readthedocs.io/zh_CN/latest/target.html   */\n        "source": "auto",       /*源语言，参照：https://pygtrans.readthedocs.io/zh_CN/latest/target.html   */\n        "proxies": {\n            "http": "http://localhost:7890",\n            "https": "http://localhost:7890"\n        }      /*代理  */\n    },\n    "BAIDUAPI":{       /*获取百度翻译api：http://api.fanyi.baidu.com/manage/developer  */\n        "appid": "114514",        /*填写你的百度翻译api的id  */\n        "secretKey": "1919810",      /*填写你的百度翻译api的秘钥  */\n        "fromLang": "auto",       /*翻译源语言，支持列表参考：http://api.fanyi.baidu.com/doc/21  */\n        "toLang": "zh"        /*翻译目标语言，支持列表参考：http://api.fanyi.baidu.com/doc/21  */\n    },\n    "TENCENTAPI": {     /*腾讯云文本翻译API：https://cloud.tencent.com/document/product/551/15611  */\n        "SecretId": "1.048596%",     /*Id  */\n        "SecretKey": "ahshitherewegoagain",    /*Key  */\n        "Target": "zh",   /*目标语言，参照：https://cloud.tencent.com/document/product/551/40566#2.-.E8.BE.93.E5.85.A5.E5.8F.82.E6.95.B0  */\n        "Source": "auto"    /*源语言，参照：https://cloud.tencent.com/document/product/551/40566#2.-.E8.BE.93.E5.85.A5.E5.8F.82.E6.95.B0  */\n    },\n    "TRANSLATOR":{          /*翻译模块  */\n        "sublevel": 20,      /*文本切割行数，一次翻译多少行，默认20。数字越小翻译越慢,而且会因为访问速度太快而无法访问api，数字过大可能会因文本量过大而无响应  */\n        "sleep_time": 0.4     /*api访问间隔，单位：秒。翻译被掐断可以尝试提高此数值。  */\n    },\n    "PACKAGE":{             /*打包模块  */\n        "cover_api": "https://api.yimian.xyz/img?type=head",     /*材质包封面图url，无法访问则使用原材质包的封面  */\n        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"     /*访问封面图url的UA配置  */\n    }\n}'
if not os.path.exists('config.json'):
    print("未找到配置文件，已为您创建，需手动修改配置文件里的id和key")
    with open('config.json', 'w', encoding='utf-8') as f:
        f.write(config)
    f.close()
config_read = ''
with open('config.json', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        # print(re.sub('/\*.+?\*/', '',i))
        config_read += re.sub('/\*.+?\*/', '',i)
    # print(config_read)
    config = json.loads(config_read)
    # print(config)
f.close()
try:
    # api = config['TRANSLATOR_API']
    target = config['GOOGLEAPI']['target']
    source = config['GOOGLEAPI']['source']
    proxies = config['GOOGLEAPI']['proxies']
    appid = config['BAIDUAPI']['appid']
    secretKey = config['BAIDUAPI']['secretKey']
    fromLang = config['BAIDUAPI']['fromLang']
    toLang = config['BAIDUAPI']['toLang']
    SecretId = config['TENCENTAPI']['SecretId']
    SecretKey = config['TENCENTAPI']['SecretKey']
    Target = config['TENCENTAPI']['Target']
    Source = config['TENCENTAPI']['Source']
    sublevel = config['TRANSLATOR']['sublevel']
    sleep_time = config['TRANSLATOR']['sleep_time']
    cover_api = config['PACKAGE']['cover_api']
    ua = config['PACKAGE']['User-Agent']
except:
    print("配置文件有误，请删除config.json并重新打开本软件")
    exit(1)


def tencent_trans(q):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)

        req = models.TextTranslateRequest()
        req.SourceText = q  # 要翻译的语句
        req.Source = Source  # 源语言类型
        req.Target = Target  # 目标语言类型
        req.ProjectId = 0

        resp = client.TextTranslate(req)
        data = json.loads(resp.to_json_string())
        # print(data['TargetText'])
        return data['TargetText']

    except TencentCloudSDKException as err:
        print(err)


# tencent_trans('apple')

def google_trans(q):
    try:
        client = Translate(proxies=proxies)
        text = client.translate(q)
        # print(text.translatedText)
        return text.translatedText
    except:
        print('err')


# google_trans('apple')
def download(file_path, picture_url):
    headers = {
        "User-Agent": ua,
    }
    r = requests.get(picture_url, headers=headers)
    with open(file_path, 'wb') as f:
        f.write(r.content)


# download('test.png','https://api.yimian.xyz/img?type=head')
def progress_bar(scale, i, progress):
    a = "*" * int(i * 50 / scale)
    b = "." * int((scale - i) * 50 / scale)
    c = (i / scale) * 100
    dur = time.perf_counter() - progress
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur), end="")
    time.sleep(0.01)
    # print("\n" + "执行结束，万幸".center(scale // 2, "-"))


# for i in range(101):
#     start = time.perf_counter()
#     progress_bar(100,i)

httpClient = None
url = '/api/trans/vip/translate'  # 通用翻译API HTTP地址

# fromLang = 'auto'  # 原文语种
# toLang = 'zh'  # 译文语种
salt = random.randint(32768, 65536)
# appid = '20190609000305977'  # 填写你的appid
# secretKey = 'ZOqsmG878A90vHfvMHD6'  # 填写你的密钥
q = ''

baidu_encode_dict = {'§a': '♢Ⓐ', '§b': '♢Ⓑ', '§c': '♢Ⓒ',
                     '§d': '♢Ⓓ', '§e': '♢Ⓔ', '§f': '♢Ⓕ',
                     '§g': '♢Ⓖ', '§k': '♢Ⓚ', '§l': '♢Ⓛ',
                     '§m': '♢Ⓜ', '§n': '♢Ⓝ', '§o': '♢Ⓞ',
                     '§r': '♢Ⓡ', '§0': '♢⓪', '§1': '♢⓵',
                     '§2': '♢⓶', '§3': '♢⓷', '§4': '♢⓸',
                     '§5': '♢⓹', '§6': '♢⓺', '§7': '♢⓻',
                     '§8': '♢⓼', '§9': '♢⓽', '\n': '♢ⓝ'}
baidu_decode_dict = {'♢Ⓐ': '§a', '♢Ⓑ': '§b', '♢Ⓒ': '§c',
                     '♢Ⓓ': '§d', '♢Ⓔ': '§e', '♢Ⓕ': '§f',
                     '♢Ⓖ': '§g', '♢Ⓚ': '§k', '♢Ⓛ': '§l',
                     '♢Ⓜ': '§m', '♢Ⓝ': '§n', '♢Ⓞ': '§o',
                     '♢Ⓡ': '§r', '♢⓪': '§0', '♢⓵': '§1',
                     '♢⓶': '§2', '♢⓷': '§3', '♢⓸': '§4',
                     '♢⓹': '§5', '♢⓺': '§6', '♢⓻': '§7',
                     '♢⓼': '§8', '♢⓽': '§9', '♢ⓝ': '\n'}

google_encode_dict = {'§a': 'Ωη', '§b': 'Ωα', '§c': 'Ωλ',
                      '§d': 'Ωυ', '§e': 'Ωε', '§f': 'Ωπ',
                      '§g': 'Ωδ', '§k': 'Ωκ', '§l': 'Ωι',
                      '§m': 'Ωμ', '§n': 'Ων', '§o': 'Ωο',
                      '§r': 'Ωσ', '\n': '☹'}

google_decode_dict = {'Ωη': '§a', 'Ωα': '§b', 'Ωλ': '§c',
                      'Ωυ': '§d', 'Ωε': '§e', 'Ωπ': '§f',
                      'Ωδ': '§g', 'Ωκ': '§k', 'Ωι': '§l',
                      'Ωμ': '§m', 'Ων': '§n', 'Ωο': '§o',
                      'Ωσ': '§r', '☹': '\n'}

tencent_encode_dict = {'§a': '|A|', '§b': '|B|', '§c': '|C|',
                       '§d': '|D|', '§e': '|E|', '§f': '|F|',
                       '§g': '|G|', '§k': '|K|', '§l': '|L|',
                       '§m': '|M|', '§n': '|N|', '§o': '|O|',
                       '§r': '|R|', '§0': '|H|', '§1': '|I|',
                       '§2': '|J|', '§3': '|P|', '§4': '|Q|',
                       '§5': '|S|', '§6': '|T|', '§7': '|U|',
                       '§8': '|V|', '§9': '|Z|', '\n': '\n'}
tencent_decode_dict = {'|A|': '§a', '|B|': '§b', '|C|': '§c',
                       '|D|': '§d', '|E|': '§e', '|F|': '§f',
                       '|G|': '§g', '|K|': '§k', '|L|': '§l',
                       '|M|': '§m', '|N|': '§n', '|O|': '§o',
                       '|R|': '§r', '|H|': '§0', '|I|': '§1',
                       '|J|': '§2', '|P|': '§3', '|Q|': '§4',
                       '|S|': '§5', '|T|': '§6', '|U|': '§7',
                       '|V|': '§8', '|Z|': '§9', '\n': '\n'}


# ηαλυ


def baidu_trans(q):
    global httpClient
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    # print(fromLang,toLang)
    myurl = url + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + \
            '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        # print(result)
        source_language = result['from']
        output_language = result['to']
        source_text = result['trans_result'][0]['src']
        output_text = result['trans_result'][0]['dst']
        # print(source_language + '  to  ' + output_language + '  :  ' + source_text + '  ===>  ' + output_text)
        return output_text

    except Exception as e:
        print(e)
        print("API出错")
    finally:
        if httpClient:
            httpClient.close()


def translator(q, api):
    if api == 1:
        return google_trans(q)
    if api == 2:
        return baidu_trans(q)
    if api == 3:
        return tencent_trans(q)


# print('1',translator('apple',1))
# print('2',translator('apple',2))
# print('3',translator('apple',3))
def getAllSub(path):
    Dirlist = []
    Filelist = []
    for home, dirs, files in os.walk(path):
        # 获得所有文件夹
        for dirname in dirs:
            Dirlist.append(os.path.join(home, dirname))
        # 获得所有文件
        for filename in files:
            Filelist.append(os.path.join(home, filename))
    return Dirlist, Filelist  # 返回所有文件夹列表和文件列表[dirlist, filelist]


# 根据keyword从flist中筛选满足条件的文件/文件夹路径

def getkwfile(flist, keyword):
    res = []
    for ff in flist:
        if keyword in ff.split('\\')[-1]:  # 切分出文件名来再判断，可以缩短判断时间
            res.append(ff)
    return res


# mcdata_path = os.path.expanduser('~') + r'\AppData\Local\Packages\Microsoft.MinecraftUWP_.*'
# os.system("explorer.exe %s" % mcdata_path)
# os.startfile(mcworld_templates)
# os.walk(mcworld_templates, topdown=False, onerror=None, followlinks=False)
def getlist(type):
    if type == 0:
        world_dict = {}
        files = os.listdir(mcworld_templates)  # 读入文件夹
        num_png = len(files)  # 统计文件夹中的文件个数\
        # print(num_png)
        getlist_time = time.perf_counter()
        print("{:=^58s}".format("加载地图列表中"))
        for i in range(num_png):
            with open(mcworld_templates + '\\' + files[i - 1] + '\\levelname.txt', 'r', encoding='utf-8') as f:
                levelname = f.read()
                world_dict[str(i + 1)] = [mcworld_templates + '\\' + files[i - 1], levelname]
            progress_bar(num_png, i + 1, getlist_time)
            # if 'levelname.txt' in files:
            #     levelname_path = str(root) + '\levelname.txt'
            #     # print(levelname_path)
            #     with open(levelname_path, "r", encoding='utf-8') as f:  # 打开文本
            #         levelname = f.read()  # 读取文本
            #         # print(levelname)
            #         x += 1
            #     f.close()
            #     i += 1
            #     world_dict[str(i)] = [str(root), levelname]
        # print(x)
        # print(world_dict)
        return world_dict
    if type == 1:
        lang_list = {}
        i = 0
        files = os.listdir(chose_pack_path + '\\resource_packs\\rp0\\texts')  # 读入文件夹
        # print(len(files))
        for root, dirs, files in os.walk(chose_pack_path + '\\resource_packs\\rp0\\texts', topdown=False, onerror=None,
                                         followlinks=False):
            for j in files:
                if ".lang" in j:
                    file_size = os.path.getsize(chose_pack_path + '\\resource_packs\\rp0\\texts\\' + j)
                    i += 1
                    lang_list[str(i)] = [j, '{:.2f}'.format(file_size / 1024)]
        return lang_list
    if type == 2:
        lang_list = {}
        i = 0
        files = os.listdir(chose_pack_path + '\\texts')  # 读入文件夹
        # print(len(files))
        for root, dirs, files in os.walk(chose_pack_path + '\\texts', topdown=False, onerror=None,
                                         followlinks=False):
            for j in files:
                if ".lang" in j:
                    file_size = os.path.getsize(chose_pack_path + '\\texts\\' + j)
                    i += 1
                    lang_list[str(i)] = [j, '{:.2f}'.format(file_size / 1024)]
        return lang_list


def read_lang(lang_path):
    with open(lang_path, encoding='utf-8') as f:
        lang = f.read()
    f.close()
    # print(lang)
    lang_key = re.findall('(.*)=', lang)
    lang_value = re.findall('=(.*)', lang)
    # print(lang_key)
    # print(lang_value)
    return lang_key, lang_value


def cut(cut_file, line_start, line_stop):
    with open(cut_file, encoding='utf-8') as f:
        txt = f.readlines()
        f.close()
    txt_temp = txt[line_start:line_stop]
    # print(txt_temp)
    re_txt = ''
    for i in range(line_stop - line_start):
        re_txt += txt_temp[i].replace('\n', encode_n[api - 1])
        # print(re_txt)
    # print(re_txt)
    return re_txt


def code(api):
    if api == 1:
        encode_dict = google_encode_dict
        decode_dict = google_decode_dict
    if api == 2:
        encode_dict = baidu_encode_dict
        decode_dict = baidu_decode_dict
    if api == 3:
        encode_dict = tencent_encode_dict
        decode_dict = tencent_decode_dict
    return encode_dict, decode_dict


def trans_save(n, api):
    txt_save = ''
    trans_time = time.perf_counter()
    if lang_value_len % n == 0:
        for i in range(int(lang_value_len / n)):
            txt = translator(cut('temp\\lang_value_fix.txt', i * n, i * n + n), api)
            # print(txt)
            progress_bar(int(lang_value_len / n), i, trans_time)
            txt_save += txt.replace(encode_n[api - 1], '\n')
            time.sleep(sleep_time)
    else:
        for i in range(int(lang_value_len / n)):
            txt = translator(cut('temp\\lang_value_fix.txt', i * n, i * n + n), api)
            # print('-------------')
            # print(txt)
            progress_bar(int(lang_value_len / n + 1), i, trans_time)
            # print('-------------')
            txt_save += txt.replace(encode_n[api - 1], '\n')
            time.sleep(sleep_time)
        txt = translator(cut('temp\\lang_value_fix.txt', int(int(lang_value_len) / 20) * 20, int(lang_value_len)), api)
        # print('------------')
        # print(txt)
        progress_bar(1, 1, trans_time)
        # print('-------------')
        txt_save += txt.replace(encode_n[api - 1], '\n')
    # print(txt_save)

    for key in decode_dict.keys():
        # print(key)
        txt_save = txt_save.replace(key, decode_dict[key])
    # print(txt_save)  # 处理源数据
    with open('temp\\lang_value_zh.txt', 'w', encoding='utf-8') as f:
        f.write(txt_save)
    f.close()


def exegesis(type, number):
    save = ''
    if number == 1:
        with open(chose_pack_path + '\\manifest.json') as f:
            path_name = json.loads(f.read())['header']['name'].replace('\\','').replace('/','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','').replace(':','')
            f.close()
    else:
        path_name = list_temp[choose_pack][1].replace('\\','').replace('/','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','').replace(':','')
    print(path_name)
    with open('temp\\lang_value_zh.txt', 'r', encoding='utf-8') as value:
        i = 0
        if type == 1:
            with open('temp\\lang_value_temp.txt', 'r', encoding='utf-8') as exe:
                exe_temp = exe.readlines()
                # print(exe_temp)
                for f in value.readlines():
                    f = lang_key_source[i] + '=' + f.strip('\n') + '###' + exe_temp[i]
                    i += 1
                    save += f
                    # print(f)
            exe.close()
        else:
            for f in value.readlines():
                f = lang_key_source[i] + '=' + f.strip('\n') + '\n'
                i += 1
                save += f
    value.close()
    if not os.path.exists(path_name):
        os.mkdir(path_name)
    with open('.\\%s\\zh_CN.lang' % path_name, 'w+', encoding='utf-8') as f:
        f.write(save)
    f.close()
    return save


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


def package(number):
    if number == 1:
        with open(chose_pack_path + '\\manifest.json') as f:
            path_name = json.loads(f.read())['header']['name'].replace('\\','').replace('/','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','').replace(':','')
            f.close()
    else:
        path_name = list_temp[choose_pack][1].replace('\\','').replace('/','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','').replace(':','')
    if not os.path.exists(path_name + ' zh_CN\\' + path_name + ' zh_CN\\' + '\\texts'):
        os.makedirs(path_name + ' zh_CN\\' + path_name + ' zh_CN\\' + '\\texts')
    with open(path_name + ' zh_CN\\' + path_name + ' zh_CN\\' + '\\texts\\zh_CN.lang', 'w+',
              encoding='utf-8') as f:
        f.write(save)
    f.close()
    languages = '["zh_CN"]'
    with open(path_name + ' zh_CN\\' + path_name + ' zh_CN\\' + '\\texts\\languages.json',
              'w', encoding='utf-8') as f:
        f.write(languages)
    f.close()
    manifest = '{"format_version": 2,"header": {"name": "%s汉化","description": "此汉化包由《Minecraft基岩版市场包汉化工具》制作","uuid": "%s","version": [1,0,0],"min_engine_version": [1,16,0]},"modules": [{"type": "resources","uuid": "%s","version": [1,8,0]}]}' % (
        path_name, uuid.uuid1(), uuid.uuid1())
    with open(path_name + ' zh_CN\\' + path_name + ' zh_CN\\' + '\\manifest.json', 'w',
              encoding='utf-8') as f:
        f.write(manifest)
    f.close()
    try:
        download(path_name + ' zh_CN\\' + path_name + ' zh_CN\\' + '\\pack_icon.png', cover_api)
    except:
        print('api出错，已使用原材质包图片')
        try:
            # print(chose_pack_path + r'\resource_packs\rp0\pack_icon.png')
            if number != 1:
                shutil.copy(chose_pack_path + '\\resource_packs\\rp0\\pack_icon.png',
                        path_name + ' zh_CN\\' + path_name + ' zh_CN\\')
            else:
                shutil.copy(chose_pack_path + '\\pack_icon.png',
                            path_name + ' zh_CN\\' + path_name + ' zh_CN\\')
        except:
            print('复制出错，材质包无封面')
    zipDir('.\\' + path_name + ' zh_CN\\' + path_name + ' zh_CN\\',
           path_name + ' zh_CN.mcpack')
    # os.rename(path_name+' zh_CN.zip',path_name+' zh_CN.mcpack')


if __name__ == '__main__':
    print("{:=^60s}".format("欢迎使用《Minecraft基岩版市场包汉化工具》"))
    print('⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⠿⣴⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢚⣩⣴⡖⣊⣁⣤⣑⠶⣥⣈⠛⢮⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣣⣾⣿⣿⡏⢹⣧⣯⠻⣿⣷⠘⣿⣿⣶⣤⣙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⡿⢡⣿⠇⣿⡏⡿⢸⣿⣿⡇⢹⣿⢿⣿⣿⣷⣏⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣸⣿⣿⠇⣼⣿⡆⠟⣧⠃⡼⣿⡟⠃⣾⡛⠀⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠈⣥⣴⠀⡏⠘⢁⠀⠙⠀⡔⡻⠀⠀⠙⠸⣇⢠⣍⡙⢛⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⡆⠀⢸⣿⠀⠀⢁⣶⠀⠀⢸⠀⢁⠀⣸⣄⠀⢾⠈⣿⣿⡿⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⡇⢰⢸⣿⡀⠀⠉⣁⠈⠃⣠⣠⣿⠂⠀⣉⠀⠈⢸⣿⣿⡇⢸⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣿⢸⡆⠘⡿⠄⠸⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⡿⠁⢉⣿⣿⡇⢸⣧⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⠟⢃⣿⡇⠀⣿⠄⢠⡘⣿⣿⣿⣿⣿⣿⣿⣿⣟⣡⠆⢸⡟⢻⠁⡟⣿⣎⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⡏⣜⣿⣿⠁⡇⢹⡇⡄⢿⣿⣿⣿⣬⣿⣥⣿⣿⣿⠏⡀⣸⠃⢿⠀⣷⡸⣿⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⡟⣼⣿⣿⡿⢠⡇⠘⡇⢸⠂⡍⠻⢿⣿⣿⣿⠿⠛⢡⢸⠁⣿⠀⠘⡄⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⡏⡾⣰⣿⣿⣿⡇⠸⢠⣇⢳⠘⢸⠃⠁⣶⣬⣉⣤⠆⠉⢸⠘⢠⠇⡀⣧⠀⢹⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⡟⡸⣱⣿⣿⣿⢿⠃⡇⢈⣡⣌⠀⣴⡆⢠⣮⣙⣛⣵⣆⢉⣆⠁⡜⣀⠃⢻⢳⣀⢻⣇⢹⣿⣷⡸⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⠑⢱⣿⣿⣿⡟⡼⠐⢠⡙⠻⣿⣆⢈⠛⢦⠻⠏⠈⠟⠡⠞⢛⠁⡰⠟⢃⡘⢇⣿⣬⣿⡄⢿⣿⡇⠹⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⠃⢠⣿⡿⢿⣿⢱⠇⣰⣿⡉⣷⠀⣍⣙⠛⠒⠀⠀⠀⠀⢒⠚⣃⡈⢰⣾⢉⣿⡄⢻⣻⣼⣧⠸⣿⣿⡄⢻⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⡏⢠⣿⣿⠇⣼⣏⡞⢰⣿⣿⣇⢸⠀⣿⣿⠀⣿⠇⣠⢸⠀⣿⠀⣿⡇⢸⡇⢸⣿⣿⡄⢹⣇⢿⡄⢿⣿⣿⡈⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⡟⢠⣿⣿⣿⢀⣿⠞⢠⣿⣿⣿⣿⠈⣀⣿⣿⠀⡿⢠⡇⢸⣆⢸⠀⢿⣿⠘⠃⣾⣿⣿⣿⣆⠻⣸⡇⢸⢿⣿⣷⡘⣿⣿⣿⣿\n⣿⣿⣿⡿⣡⣿⣿⣿⡇⣸⣏⣦⡐⠌⡙⠻⣿⡇⢻⣿⡿⠀⠇⣼⡇⢸⣿⠈⡇⢸⣿⡆⢰⡿⠟⢉⠡⢂⣴⡇⣿⠘⣏⢻⣿⣷⡙⣿⣿⣿\n⣿⣿⡿⣱⣿⡟⣼⢿⠀⣿⣸⣿⣿⠂⣿⣷⣤⡁⣼⣿⣷⠄⣼⣿⡇⠸⣿⣇⠠⣴⣿⡧⢈⣴⣾⣿⠀⣿⣯⢸⢼⡀⣿⣧⠻⣿⣿⡜⣿⣿\n⣿⡟⣼⣿⢫⣾⢯⣾⢠⡇⡟⢸⣿⠀⣿⣿⣿⠀⣻⠟⣡⣾⡿⠋⡠⢀⠙⢿⣧⡈⢿⡇⢸⣿⣿⣿⠀⣿⣿⢸⡿⡇⣿⣿⣷⡙⣿⣿⣎⢻\n⢫⣾⡿⣱⠟⡵⢡⡎⢸⢿⠁⣿⣿⠀⣿⣿⡿⢀⣡⣾⣿⠋⢠⣾⡇⣿⣷⡈⠻⣿⣦⣉⠸⣿⣿⣿⠀⣿⣿⠘⣷⡇⢼⣏⢻⣿⣮⡻⣿⣷\n⣿⢏⣼⣿⠞⢠⣿⡇⢸⣿⠨⣿⣿⢰⡟⢡⣴⣿⣿⡟⡅⣰⣿⣿⣷⣿⣿⡍⣆⠹⣿⣿⣷⣤⡙⢿⠀⣿⡟⠀⢿⡇⡈⢿⣆⢙⢿⣷⣌⢻\n5oS/5L2g5pyJ5LiA5aSp6IO95LiO5L2g5pyA6YeN6KaB55qE5Lq66YeN6YCi')
    print("{:=^60s}".format("让艾拉来为你祈祷API链接通畅吧！"))
    print("本工具完全开源免费\n欢迎来我的个人博客联系我：haru.vip")
    print("{:=^60s}".format(""))
    while True:
        print('请选择翻译API：\n(1) Google\n(2) Baidu\n(3) Tencent')
        input_number = input('请输入序号：')
        try:
            int(input_number)
        except ValueError:
            print('请输入序号！')
            continue
        if int(input_number) <= 0 or int(input_number) > 3:
            print('输入有误，请重新输入！')
            continue
        else:
            break
    api = int(input_number)
    encode_dict, decode_dict = code(api)
    # print(encode_n[api-1])
    while True:
        print("{:=^60s}".format(""))
        print("请选择模式\n(1) 自动扫描已下载市场包\n(2) 输入需翻译的材质包路径")
        while True:
            input_number = input('请输入序号：')
            try:
                int(input_number)
            except ValueError:
                print('请输入序号！')
                continue
            if int(input_number) <= 0 or int(input_number) > 2:
                print('输入有误，请重新输入！')
                continue
            else:
                break
        if int(input_number) == 2:
            print("{:=^60s}".format(""))
            print(
                "文件结构需如下图所示：\n  │manifest.json\n  │pack_icon.png\n  └─texts\n       │'test1'.lang\n       │'test2'.lang\n       │'test3'.lang\n       │...")
            while True:
                input_path = input('请输入路径：')
                if not os.path.exists(input_path):
                    print("路径不存在，请重新输入")
                    continue
                else:
                    if not os.path.exists(input_path + '\\texts'):
                        print("texts文件夹不存在，请重新输入")
                        continue
                    if not os.path.exists(input_path + '\\manifest.json'):
                        print("manifest.json文件不存在，请重新输入")
                        continue
                    if not os.path.exists(input_path + '\\pack_icon.png'):
                        print("pack_icon.png文件不存在，请重新输入")
                        continue
                    break
            chose_pack_path = input_path
            lang_list = getlist(2)
            print("{:=^50s}".format(""))
            for key in lang_list:
                print('(' + str(key) + ')', lang_list[key][0], lang_list[key][1] + 'Kb')  # 输出lang文件列表
            print("{:=^50s}".format("建议选择尽可能大的文件"))
            print('ps: 通常选择en_US.lang就可以了')
            while True:
                input_number = input('请输入序号：')
                try:
                    int(input_number)
                except ValueError:
                    print('请正确输入序号！')
                    continue
                if int(input_number) <= 0 or int(input_number) > int(key):
                    print('输入有误，请重新输入！')
                    continue
                else:
                    break
            lang_path = chose_pack_path + '\\texts\\' + lang_list[input_number][0]
            print("{:=^50s}".format(""))
            lang_key_source, lang_value = read_lang(lang_path)
            with open('temp\\lang_value_temp.txt', 'w', encoding='utf-8') as f:
                for value in lang_value:
                    f.write(value + '\n')
            f.close()
            for key in encode_dict.keys():
                x = 0
                for fix in lang_value:
                    lang_value[x] = fix.replace(key, encode_dict[key])
                    lang_value[x] = re.sub('#.*', '', lang_value[x])
                    # print(lang_value[x])
                    x += 1
            # print(lang_value)  # 处理源数据
            temp = ''
            for j in lang_value:
                temp = temp + j + '\n'
            with open('temp\\lang_value_fix.txt', 'w', encoding='utf-8') as f:
                f.write(temp)
            f.close()
            # print(translator(temp))
            lang_value_len = len(lang_value)
            print("{:=^50s}".format("翻译中，请耐心等待"))
            trans_save(int(sublevel), api)
            print("\n{:=^50s}".format("翻译完成"))
            print("是否需要原文注释？\n(1) 是\n(2) 否")
            while True:
                input_number = input('请输入序号：')
                try:
                    int(input_number)
                except ValueError:
                    print('请正确输入序号！')
                    continue
                if int(input_number) <= 0 or int(input_number) > 2:
                    print('输入有误，请重新输入！')
                    continue
                else:
                    break
            if int(input_number) == 1:
                save = exegesis(1, 1)
            else:
                save = exegesis(0, 1)
            # print(save)
            with open(chose_pack_path + '\\manifest.json') as f:
                path_name = json.loads(f.read())['header']['name'].replace('\\','').replace('/','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','').replace(':','')
                f.close()
            print('已保存至“%s\zh_CN.lang”！' % path_name)
            print("是否需要打包成.mcpack文件\n(1) 是\n(2) 否")
            while True:
                input_number = input('请输入序号：')
                try:
                    int(input_number)
                except ValueError:
                    print('请正确输入序号！')
                    continue
                if int(input_number) <= 0 or int(input_number) > 2:
                    print('输入有误，请重新输入！')
                    continue
                else:
                    break
            if int(input_number) == 1:
                package(1)
            print('DONE！')
            input('')
            break
        else:
            path = os.path.expanduser('~') + '\\AppData\\Local\\Packages'  # 查找地址
            keyword = 'MinecraftUWP'  # 关键字
            subList = getAllSub(path)[0] + getAllSub(path)[1]
            resList = getkwfile(subList, keyword)
            # print(len(resList))
            # print(resList[0])
            mcdata_path = str(resList[0])
            mcworld_templates = mcdata_path + '\\LocalState\\premium_cache\\world_templates'
            # print(mcworld_templates)

            list_temp = getlist(0)
            # print(list_temp)
            print("\n{:=^60s}".format("加载完成"))
            for key in list_temp:
                print('(' + str(key) + ')', list_temp[key][1])  # 输出存档列表
                # print(list_temp[key][1])
            print("{:=^60s}".format(""))
            # print(key)
            while True:
                input_number = input('请输入序号：')
                try:
                    int(input_number)
                except ValueError:
                    print('请输入序号！')
                    continue
                if int(input_number) <= 0 or int(input_number) > int(key):
                    print('输入有误，请重新输入！')
                    continue
                else:
                    break
            print("{:=^50s}".format("语言文件列表"))
            choose_pack = input_number
            # print(choose_pack)
            chose_pack_path = list_temp[str(input_number)][0]
            # print(chose_pack_path)  # 输出选择的存档路径

            # print(getlist(1))
            lang_list = getlist(1)
            # print("{:=^50s}".format(""))
            for key in lang_list:
                print('(' + str(key) + ')', lang_list[key][0], lang_list[key][1] + 'Kb')  # 输出lang文件列表

            print("{:=^50s}".format("建议选择尽可能大的文件"))
            print('ps: 通常选择en_US.lang就可以了')
            while True:
                input_number = input('请输入序号：')
                try:
                    int(input_number)
                except ValueError:
                    print('请正确输入序号！')
                    continue
                if int(input_number) <= 0 or int(input_number) > int(key):
                    print('输入有误，请重新输入！')
                    continue
                else:
                    break

            lang_path = chose_pack_path + '\\resource_packs\\rp0\\texts\\' + lang_list[input_number][0]
            print("{:=^50s}".format(""))
            lang_key_source, lang_value = read_lang(lang_path)
            with open('temp\\lang_value_temp.txt', 'w', encoding='utf-8') as f:
                for value in lang_value:
                    f.write(value + '\n')
            f.close()
            for key in encode_dict.keys():
                x = 0
                for fix in lang_value:
                    lang_value[x] = fix.replace(key, encode_dict[key])
                    lang_value[x] = re.sub('#.*', '', lang_value[x])
                    # print(lang_value[x])
                    x += 1
            # print(lang_value)  # 处理源数据
            temp = ''
            for j in lang_value:
                temp = temp + j + '\n'
            with open('temp\\lang_value_fix.txt', 'w', encoding='utf-8') as f:
                f.write(temp)
            f.close()
            # print(translator(temp))
            lang_value_len = len(lang_value)
            print("{:=^50s}".format("翻译中，请耐心等待"))
            trans_save(int(sublevel), api)
            print("\n{:=^50s}".format("翻译完成"))
            print("是否需要原文注释？\n(1) 是\n(2) 否")
            while True:
                input_number = input('请输入序号：')
                try:
                    int(input_number)
                except ValueError:
                    print('请正确输入序号！')
                    continue
                if int(input_number) <= 0 or int(input_number) > 2:
                    print('输入有误，请重新输入！')
                    continue
                else:
                    break
            if int(input_number) == 1:
                save = exegesis(1, 0)
            else:
                save = exegesis(0, 0)

            print('已保存至“%s\\zh_CN.lang”！' % list_temp[choose_pack][1].replace('\\','').replace('/','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','').replace(':',''))
            print("是否需要打包成.mcpack文件\n(1) 是\n(2) 否")
            while True:
                input_number = input('请输入序号：')
                try:
                    int(input_number)
                except ValueError:
                    print('请正确输入序号！')
                    continue
                if int(input_number) <= 0 or int(input_number) > 2:
                    print('输入有误，请重新输入！')
                    continue
                else:
                    break
            if int(input_number) == 1:
                package(0)
            print('DONE！')
            input('')
            break
