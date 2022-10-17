# urltrim

## 说明

​		没啥实质性的功能,只是之前处理一大堆url的时候,不同需求得整不同的脚本,感觉很麻烦,所以整合了一下,名字也是乱起的,代码是快快地整完的,只是测试了下基本功能,BUG什么的没遇到,如果使用时遇到了BUG,自己解决,扫描的话估计会有误报

## 简单功能

```
简单url处理 : 
   自动去重
   收集包含关键字的url(-r)
   去除包含关键字的url(-m)
   url裁剪(-c)
   url前拼接(-fa)
   url后拼接(-ea)
   存活检测(-s)
   线程设置(-t)
```

## 参数说明

### -f, --file

选择文件

### -r, --retrieval

从文本中挑选出包含关键字的url,多个关键字使用逗号(,)隔开

### -c, --cut

如果url中包含关键字,则将url中的关键字替换为空,多个关键字使用逗号(,)隔开

###  -m, --move

如果url中包含关键字,则删除url,多个关键字使用逗号(,)隔开

### -fa, --fadd

在每个url前面添加关键字

### -ea, --eadd

在每个url后面添加关键字

### -s, --scan

url状态码检测,多个状态码使用逗号(,)隔开

(本来想弄成直接200,后来想起来可能会有其他状态码需求,所以设置为写参数了,不好的一点就是必须带参数了)

### -t, --thread

线程设置,默认50,只有进行状态码检测的时候才有用

## 系统流程

​		主程序是urlTrim类中的main方法,大致流程就是判断传入的参数:`打开文件并自动去重 -> 检测是否需要挑选携带关键字的url -> 检测是否需要裁剪url -> 检测是否需要删除携带关键字的url -> 检测url首位是否需要添加内容 -> 检测url末尾是否需要添加内容 -> 检测是否需要进行扫描 -> 写入结果文件`

流程是随便设置的,使用哪个功能就用那个

## 简单使用

### 只进行去重

```shell
python3 urltrim.py -f qiqi.txt
```

### 挑选带有关键字的url

```shell
python3 urltrim.py -f qiqi.txt -r 8080,9090
```

### 裁剪url

```shell
去除url中的http://和https://
python3 urltrim.py -f qiqi.txt -c http://,https
```

### 删除携带关键字的url

```shell
比如说删除掉携带test的url
python3 urltrim.py -f qiqi.txt -m test
```

### url首位添加内容(只能添加一个)

```shell
如果想在ip+端口组合前面加上http://
python3 urltrim.py -f qiqi.txt -fa http://
```

### url末尾添加内容(只能添加一个)

```shell
如果想在url末尾添加内容
python3 urltrim.py -f qiqi.txt -ea /login
```

### url状态码检测

```shell
挑选出状态码为200的url
python3 urltrim.py -f qiqi.txt -s 200

挑选出状态码为200或404的url
python3 urltrim.py -f qiqi.txt -s 200,404
```

### 设置扫描线程

```shell
python3 urltrim.py -f qiqi.txt -s 200 -t 10
```

## 组合使用

​		如果qiqi.txt中的url都是ip+port组合,想要在前面加上http://,在后面加上/login,去掉带gov,edu的网站,最后进行状态码200检测,设置线程为10

```shell
python3 urltrim.py qiqi.txt -fa http:// -ea /login -m .gov,.edu -s 200 -t 10
```

结果会保存在url文件同目录下,格式为:名字_result.txt

**注:由于内部未添加poc,不能做漏洞验证**

