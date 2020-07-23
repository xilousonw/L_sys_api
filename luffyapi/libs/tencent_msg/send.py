from qcloudsms_py import SmsSingleSender
from luffyapi.utils.logger import log
from . import setting

def get_code():
    import random
    msg_code = ''
    for i in range(4):
        msg_code += str(random.randint(0,9))
    return msg_code


def send_msg(phone,code):

    ssender = SmsSingleSender(setting.appid, setting.appkey)
    params = [code, '3']
    try:
        result = ssender.send_with_param(86, phone, setting.template_id,params, sign=setting.sms_sign, extend="", ext="")
        if result.get('result'):
            return True
        else:
            return False
    except Exception as e:
        log.error('手机号：%s,短信发送失败，错误为: %s'%(phone,str(e)))