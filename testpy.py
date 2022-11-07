from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
import time

#蓝牙传输
def servo_init():#初始化指令
    bd_addr = "20:16:08:08:39:75" #arduino连接的蓝牙模块的地址
    port = 1
     
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port)) #创建连接
     
    sock.send("1") #发送数据
    sock.close()  #关闭连接
    
def bt_open():#开门指令
    bd_addr = "20:16:08:08:39:75" 
    port = 1
     
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port)) 
     
    sock.send("2") 
    sock.close()  

def bt_close():#关门指令
    bd_addr = "20:16:08:08:39:75" 
    port = 1
     
    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port)) 
     
    sock.send("3") 
    sock.close()    

#百度人脸识别API账号信息
APP_ID = '15050553'
API_KEY = 'rlRrtRL5oRdXGh71jgg1OmyN'
SECRET_KEY ='dK5TpuTAZn2nw5eVpspZLmF5Qs1Uu8A1'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)#创建一个客户端用以访问百度云
#图像编码方式
IMAGE_TYPE='BASE64'
camera = PiCamera()#定义一个摄像头对象
#用户组
GROUP = 'lihuaqiang'
 
#照相函数
def getimage():
    camera.resolution = (1024,768)#摄像界面为1024*768
    camera.start_preview()#开始摄像
    time.sleep(2)
    camera.capture('faceimage.jpg')#拍照并保存
    time.sleep(2)
#对图片的格式进行转换
def transimage():
    f = open('faceimage.jpg','rb')
    img = base64.b64encode(f.read())
    return img
#上传到百度api进行人脸检测
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP);#在百度云人脸库中寻找有没有匹配的人脸
    if result['error_msg'] == 'SUCCESS':#如果成功了
        name = result['result']['user_list'][0]['user_id']#获取名字
        score = result['result']['user_list'][0]['score']#获取相似度
        if score > 80:#如果相似度大于80
            if name == '_01lihuaqiang':
 
                print("欢迎%s !" % name)
                time.sleep(3)
            if name == '_01jishiershi':
                print("欢迎%s !" % name)
                time.sleep(3)
            if name == "_01quhao":
                print("欢迎%s !" % name)
        else:
            print("对不起，我不认识你！")
            name = 'Unknow'
            return 0
        curren_time = time.asctime(time.localtime(time.time()))#获取当前时间
 
        #将人员出入的记录保存到Log.txt中
        f = open('Log.txt','a')
        f.write("Person: " + name + "     " + "Time:" + str(curren_time)+'
')
        f.close()
        return 1
    if result['error_msg'] == 'pic not has face':
        print('检测不到人脸')
        time.sleep(2)
        return 0
    else:
        print(result['error_code']+ result['error_code'])
        return 0
#主函数
if __name__ == '__main__':
    while True:
        print('准备')
        if True:
            getimage()#拍照
            img = transimage()#转换照片格式
            res = go_api(img)#将转换了格式的图片上传到百度云
            if(res == 1):#是人脸库中的人
                print("开门")
            else:
                print("关门")
            print('稍等三秒进入下一个')
            time.sleep(3)
