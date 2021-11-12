import re
import subprocess
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-o")#下载目标文件夹
parser.add_argument("-f")#还没用
parser.add_argument("-e")
args = parser.parse_args()

file_path = args.o


def read_filename_from_txt(target):
    filename = None
    for line in artists:
        if target in line:
            if ',' in line:
                filename = line.split(',')[1]
    return filename
    

def filename_generator(filename):
    time1 = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    if 'youtube' in filename:
        short_filename = read_filename_from_txt(filename)
        if short_filename == None:
            short_filename = filename[-11:] + time1 + ".ts"
    elif 'bilibili' in filename:
        short_filename = read_filename_from_txt(filename)
        if short_filename == None:
            pattern = re.compile(r'https://live.bilibili.com/([0-9a-zA-Z\_-]+)')
            short_filename = pattern.search(filename)[1] + time1 + ".ts"
    elif 'twitch' in filename:
        short_filename = read_filename_from_txt(filename)
        if short_filename == None:
            pattern = re.compile(r'https://www.twitch.tv/([0-9a-zA-Z\_-]+)')
            short_filename = pattern.search(filename)[1] + time1 + ".ts"
    elif 'pixiv' in filename:
        #https://sketch.pixiv.net/@junkato/lives
        short_filename = read_filename_from_txt(filename)
        if short_filename == None:
            pattern = re.compile(r'https://sketch.pixiv.net/@([0-9a-zA-Z\_-]+)')
            short_filename = pattern.search(filename)[1] + time1 + ".ts"
    else:#其他名称
        short_filename = read_filename_from_txt(filename)
        short_filename = short_filename + time1 + ".ts"
    return file_path + short_filename

def pixiv_get_artist_name_from_url(artist_main_page):
    pattern = re.compile(r'https://sketch.pixiv.net/@([0-9a-zA-Z\_-]+)')
    artist_name = pattern.search(artist_main_page)[1]
    return artist_name

#考虑到可能会手动开别的streamlink，所以逻辑改为开cmd之前找一次，开完cmd之后再找一次，比较两者的差异
def get_streamlink_pid_new():
    cmd = "tasklist"
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    infos = out.stdout.read().splitlines()
    current_stream_pid_list = []
    #infos的前三行是表格的标题，所以省略
    for i in infos[3:]:
        pid_i = str(i)
        #这个正则表达式后面加了括号表示或的关系，但是也被包括进去了
        # 以第一个[0]解决的是findall的list，下面的[0]是因为前面是Pid后面是services或者console，选第一个
        result = re.findall(r'streamlink\.exe\s+([0-9]+)', pid_i)
        if result == []:
            pass
        else:
            current_stream_pid_list.append(result[0])
    #找到所有添加完了，开始比较
    return current_stream_pid_list

def get_target_m3u8(artist_name, artist_id):
    #https://sketch.pixiv.net/@chit2553/lives/1851352306408316726
    #https://sketch.pixiv.net/@yoshikadu/lives/825561229801201329
    url = "https://sketch.pixiv.net/@" + artist_name + "/lives/" + artist_id
    cmd = "powershell ./gg.ps1 -url " + url
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    result = out.stdout.read()
    return result
    
def proxy_wget(url):
    cmd = "powershell ./gl.ps1 -url " + url
    #cmd2 = "powershell Invoke-WebRequest sketch.pixiv.net -SessionVariable "
    out = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    result = out.stdout.read()
    #和request得到的应该是一样的结果
    return result
    
def show_all_pid():
    cmd = "tasklist"
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    infos = out.stdout.read().splitlines()
    pid_list = []
    #infos的前三行是表格的标题，所以省略
    for i in infos[3:]:
        pid_i = str(i)
        #这个正则表达式后面加了括号表示或的关系，但是也被包括进去了
        # 以第一个[0]解决的是findall的list，下面的[0]是因为前面是Pid后面是services或者console，选第一个
        result = re.findall(r'([0-9]+)\s(Services|Console)', pid_i)[0]
        pid_list.append(result[0])
    return pid_list

#这个用于判断主播是否下线，如果下线了，那就移除recording_list
def check_alive(stream_pid, recording_list_name_and_pid):
    flag = True
    #check pid
    current_pid_list = show_all_pid()
    #把对应的pid移出name_and_pid_list，还要把stream_pid_list也移除出去
    if stream_pid not in current_pid_list:
        print('remove id: ' + str(stream_pid))
        stream_pid_list.remove(stream_pid)
        #找到记录表里的那个已经不存在的stream_pid的位置，然后移除整条信息
        for i in recording_list_name_and_pid:
            if stream_pid == i[2]:
                try:
                    name_pid_list.remove(i)
                except:
                    pass

#进pixiv主页，把他们的id给扒下来
#<a class="thumb" href="/@horosuken/lives/5290106517565302048">
def start_record_main():
    #还没给特殊符号加斜杠
    for artist_name in artists:
        artist_name = artist_name.split(",")[0]
        #有可能是三兄弟，也有可能是Pixiv，这里分流
        if 'youtube' in artist_name:
            get_user_and_record_youtube(artist_name)
        elif 'bilibili' in artist_name:
            get_user_and_record_youtube(artist_name)
        elif 'twitch' in artist_name:
            get_user_and_record_youtube(artist_name)
        elif 'pixiv' in artist_name:
            get_user_and_record_pixiv(artist_name)
        else:
            get_user_and_record_youtube(artist_name)
            
def get_user_and_record_pixiv(artist_name):
    full_artist_name = artist_name
    artist_name = pixiv_get_artist_name_from_url(artist_name)
    try:
        #page_soup = str(proxy_wget(PIXIV_SKETCH_URL))
        proxy_wget(PIXIV_SKETCH_URL)
        f = open('temp_result.txt' ,encoding='utf-8')
        page_soup = f.read()
        f.close()
    except:
        print("Can't connect pixiv, please check your network.")
        return None 
    record_flag = True
    pattern_id = re.compile(r'<a class="thumb" href="/@' + artist_name + '/lives/(\d+)">')
    artist_id = pattern_id.search(page_soup)
    for i in name_pid_list:
        if full_artist_name in i:
            record_flag = False
    if artist_id == None:
        record_flag = False
    if record_flag == True:
        print(artist_id[1])
        pattren_m3u8 = re.compile(r'"' + artist_id[1] + '":{"finished_at"' + '\S+' +'hls_movie\S{3}(\S+m3u8)\S+' + '"web","id":"' + artist_id[1] + '",')
        artist_m3u8 = pattren_m3u8.search(page_soup)
        #m3u8url = re.findall(r'hls_movie\S{3}(\S+m3u8)', page_request)[0]
        #artist_id[1]是某个人的数字ID
        #aritst_m3u8[1]是没有去掉u002F的 m3u8链接
        if artist_m3u8 == None:
        #找不到的话就进个人主页找
            get_target_m3u8(artist_name, artist_id[1])
            f = open('artist_m3u8.txt', encoding='utf-8')
            content = f.read()
            pattren_target_m3u8 = re.compile(r'hls_movie\S{3}(\S+m3u8)')
            artist_m3u8 = pattren_target_m3u8.search(content)
            f.close()
        if artist_m3u8 == None:
            print("Find user id, but cant find .m3u8.")
        else:
            print(artist_m3u8[1].replace("\\u002F", '/'))
            recorded_filename = filename_generator(full_artist_name)
            old_streamlink_pid_list = get_streamlink_pid_new()
            #print("old")
            #print(old_streamlink_pid_list)
            cmd = "streamlink " + artist_m3u8[1].replace("\\u002F", '/') + " best " + "-o " + recorded_filename
            print(cmd)
            temp_record = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            time.sleep(8)
            print("now recording: " + artist_name)
            #print("new")
            new_streamlink_pid_list = get_streamlink_pid_new()
            #print(new_streamlink_pid_list)
            new_streamlink_pid = list(set(new_streamlink_pid_list) - set(old_streamlink_pid_list))
            if new_streamlink_pid == []:
                print("streamlink doesnt start! name is" + artist_name +" . ")
            else:
                stream_pid_list.append(new_streamlink_pid[0])
                name_pid_list.append((full_artist_name, temp_record.pid, new_streamlink_pid[0]))
#初始化
def get_user_and_record_youtube(artist_name):
    record_flag = True
    for i in name_pid_list:
        if artist_name in i:
            record_flag = False
    if record_flag == True:
        recorded_filename = filename_generator(artist_name)
        old_streamlink_pid_list = get_streamlink_pid_new()
        #print("old")
        #print(old_streamlink_pid_list)
        cmd = "streamlink " + artist_name + " best " + "-o " + recorded_filename
        temp_record = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(8)
        print("now recording: " + artist_name)
        #print("new")
        new_streamlink_pid_list = get_streamlink_pid_new()
        #print(new_streamlink_pid_list)
        new_streamlink_pid = list(set(new_streamlink_pid_list) - set(old_streamlink_pid_list))
        if new_streamlink_pid == []:
            print("streamlink doesnt start! name is" + artist_name +" . ")
        else:
            stream_pid_list.append(new_streamlink_pid[0])
            name_pid_list.append((artist_name, temp_record.pid, new_streamlink_pid[0]))

artists = []
name_pid_list = []
stream_pid_list = []
count = 0
PIXIV_SKETCH_URL = "https://sketch.pixiv.net/lives"
CHECK_INTERVAL = '60'
for line in open("pixiv.txt", 'r'):
    artists.append(line.replace('\n','').replace(' ',''))

#总循环，每过一定时间进行一次判断
while 1 > 0:
    count += 1
    recording_list = []
    offline_list = []
    print("starting " + "round " + str(count) + " ")
    start_record_main()
    record_status = ""
    #name_pid_list (name, pid)

    for i in name_pid_list:
        recording_list.append(i[0])
    for i in artists:
        if i not in recording_list:
            offline_list.append(i)
            
    record_status += "Recording: "
    for i in recording_list:
        record_status = record_status + " " + i + ","
    record_status = record_status[:-1] + ". "
    record_status += "Offline:"
    for i in offline_list:
        record_status = record_status + " " + i + ","
    record_status = record_status[:-1] + "."
    print(record_status)
    print(name_pid_list)

    #展示完一轮数据之后，休眠，然后再检查一遍有无离线，开始新的一轮
    time.sleep(int(CHECK_INTERVAL))
    print("checking offline")
    for i in name_pid_list:
        #i[2]是streamid，只要这个消失了，i[1]的pid也消失了
        check_alive(i[2], name_pid_list)