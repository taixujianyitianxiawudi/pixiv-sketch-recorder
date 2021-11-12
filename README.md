# pixiv-sketch-recorder

# usage
step1</br>
in https://sketch.pixiv.net/lives, replace the contents of cookies.txt by your own cookies.</br>
You can't record r18 streamers if you don't replace your cookies.</br>
cookie sample:   cookie_name,cookie_value,domain </br>
so please add your cookie value between the ',' (replace cookie_value)</br>

step2</br>
in pixiv.txt, add the stream http link of the streamer you want to record.</br>
example: </br>
https://sketch.pixiv.net/@ffgs10/lives </br>
https://www.youtube.com/watch?v=tqM3I2aKkIA </br>
https://www.twitch.tv/guanweiboy </br>
https://live.bilibili.com/23516237 </br>
one line one streamer </br>

step3</br>
-o \[path\]</br>
How to change download path: add -o and your dir</br>
example: ./mix -o path/to/download/


type ./mix in your powershell, enjoy!


# 使用方法

一、打开浏览器进 https://sketch.pixiv.net/lives ， 在浏览器里找到自己的cookie，替换到cookies.txt里</br>
，具体的cookie名见cookies.txt里的，总共有两个</br>
不替换cookies无法录制r18视频</br>
cookie用逗号分隔，格式 cookie_name,cookie_value,domain</br>
所以将你找到的值添加在两个逗号之间


step2</br>
在pixiv.txt里,添加你想要录制的直播链接，具体的格式见下.</br>
例子: </br>
https://sketch.pixiv.net/@ffgs10/lives </br>
https://www.youtube.com/watch?v=tqM3I2aKkIA </br>
https://www.twitch.tv/guanweiboy </br>
https://live.bilibili.com/23516237 </br>
一行一个地址</br>

step3</br>
-o \[path\]</br>
改变输出地址，在命令行里打 -o 你要下的地址 </br>
例子: ./mix -o path/to/download/

切到对应的文件夹，在powershell里打 ./mix就能运行啦

里面的request写法很鬼畜是因为要支持代理，本来能够request.get的一定得绕一下用powershell Invoke-WebRequest.
