import textwrap
import argparse
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import prettytable as pt

class urlTrim:
	def __init__(self, **kwargs):
		self.filename = kwargs["filename"]
		self.cut_str = kwargs["cut_str"]
		self.move_str = kwargs["move_str"]
		self.scan = kwargs["scan"]
		self.f_add = kwargs["f_add"]
		self.e_add = kwargs["e_add"]
		self.conn_thread = kwargs["conn_thread"]
		self.scan_code = kwargs["scan"]
		self.retrieval_str = kwargs["retrieval"]

#主程序,会自动根据参数执行相应的功能
	def main(self):
		self.banner()
		url_list = self.openfile(self.filename, "r")
		if self.retrieval_str:
			url_list = self.retrieval(url_list)
			url_list = list(set(url_list))
			print(f"剩余url: {len(url_list)}")
		if self.move_str:
			url_list = self.remove_url(url_list)
			url_list = list(set(url_list))
			print(f"剩余url: {len(url_list)}")
		if self.cut_str:
			url_list = self.cut_strs(url_list)
			url_list = list(set(url_list))
		if self.f_add:
			url_list = self.add_str(url_list, "f")
			url_list = list(set(url_list))
			print(f"[+] 首位添加 {self.f_add} +=> 完事")
		if self.e_add:
			url_list = self.add_str(url_list, "e")
			url_list = list(set(url_list))
			print(f"[+] 末尾添加 {self.e_add} +=> 完事")
		if self.scan:
			self.scan_code_list = self.scan_code.split(",")
			print(f"[+] 检测状态码: {self.scan_code}")
			self.scan_result = []
			self.scan_url(url_list)
			url_list = self.scan_result
			url_list = list(set(url_list))
			#打印扫描结果列表
			print(self.tb)
			print(f"[+] 已检测出{len(url_list)}个符合要求的URL")

		result_filename = self.filename.rsplit(".txt", 1)[0] + "_result.txt"
		self.openfile(result_filename, "w", url_list)

#读写文件
	def openfile(self, filename, mode, listx = []):
		with open(f"{filename}",mode=f"{mode}",encoding="UTF-8") as f:
			if mode == "r":
				url_list = f.read().split("\n")
				if "" in url_list:
					url_list.remove("")
				print(f"[+] 去重前: {len(url_list)}", end="  +=>  ")
				listx = list(set(url_list))
				print(f"去重后: {len(listx)}")
				return listx

			else:
				for i in listx:
					f.write(i + "\n")

#收集包含关键字的url
	def retrieval(self, url_list):
		retrieval_str_list = self.retrieval_str.split(",")
		print(f"[+] 收集包含以下内容的URL: {self.retrieval_str}", end="  +=>  ")
		index = 0
		listx = []
		while index < len(url_list):
			for retrieval_str in retrieval_str_list:
				if retrieval_str in url_list[index]:
					listx.append(url_list[index])
					break
			index += 1
		return listx

#删除包含关键字的url,为了防止索引出错,这里选择用while循环,内部嵌套for+else,如果for循环被break,不会执行break中的index += 1,如果没被break,则会执行
	def remove_url(self, url_list):
		remove_str_list = self.move_str.split(",")
		print(f"[+] 去除包含以下内容的URL: {self.move_str}", end="  +=>  ")
		index = 0
		while index < len(url_list):
			for remove_str in remove_str_list:
				if remove_str in url_list[index]:
					del url_list[index]
					break
			else:
				index += 1
		return url_list

#url裁剪
	def cut_strs(self, url_list):
		cut_str_list = self.cut_str.split(",")
		print(f"[+] 将去掉每个url中的{self.cut_str}", end=" 	 +=>	 ")
		for index,url in enumerate(url_list):
			for cut_str in cut_str_list:
				if cut_str in url:
					url_list[index] = url_list[index].replace(cut_str, "")
		if "" in url_list:url_list.remove("")
		print("完事")
		return url_list

#访问url
	def url_conn(self, url):
		print(f"[*] 正在检测{url}")
		try:
			res_code = requests.get(url, timeout=5, verify=False, allow_redirects=False).status_code
			if str(res_code) in self.scan_code_list:
				self.scan_result.append(url)
				self.tb.add_row([url, res_code])
				return f"[+] {url} 状态码为 {res_code}"
			else:
				return f"[-] {url} 状态码不符合要求"
		except Exception as e:
			return f"[-] {url} 访问超时"

#url存活检测
	def scan_url(self, url_list):
		#创建个列表
		self.tb = pt.PrettyTable(["URL","status_code"])
		self.tb.align["URL"] = "l"
		#使用线程池
		with ThreadPoolExecutor(max_workers=self.conn_thread) as pool:
			futures = [pool.submit(self.url_conn, url) for url in url_list]
			for future in as_completed(futures):
				print(future.result())

#url拼接
	def add_str(self, url_list, mode):
		for index, url in enumerate(url_list):
			if mode == "f":
				if url.startswith(self.f_add) or url == "":pass
				url_list[index] = self.f_add + url_list[index]
			else:
				if url.endswith(self.e_add) or url == "":pass
				url_list[index] += self.e_add
		if "" in url_list: url_list.remove("")
		return url_list

#banner信息
	def banner(self):
		banner = r'''
             _             _       
            | |  _        (_)      
 _   _  ____| |_| |_  ____ _ ____  
| | | |/ ___) (_   _)/ ___) |    \ 
| |_| | |   | | | |_| |   | | | | |
|____/|_|    \_) \__)_|   |_|_|_|_|

                              description: URL处理
                              author: 邪王真视守卫
												 '''
		print(banner)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='''
简单url处理 : 
	自动去重
	收集包含关键字的url(-r)
	去除包含关键字的url(-m)
	url裁剪(-c)
	url前拼接(-fa)
	url后拼接(-ea)
	存活检测(-s)
	线程设置(-t)''',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''example:
            python3 urltrim.py -f qiqi.txt -m test -c http://,https://
            '''))
	parser.add_argument("-f", "--file", dest="file", type=str, required=True, help=" example: qiqi.txt")
	parser.add_argument("-c", "--cut", dest="cut", type=str, default="", help=" example: qiqi.txt")
	parser.add_argument("-m", "--move", dest="move", type=str, default="", help=" example: test")
	parser.add_argument("-fa","--fadd", dest="fadd", type=str, default="", help=" example: http://,https://")
	parser.add_argument("-ea","--eadd", dest="eadd", type=str, default="", help=" example: /login")
	parser.add_argument("-s", "--scan", dest="scan", type=str, default="", help=" example: 200")
	parser.add_argument("-r", "--retrieval", dest="retrieval", type=str, default="", help=" example: qiqi")
	parser.add_argument("-t", "--thread", dest="thread", type=int, default=50, help=" example: 20")
	args = parser.parse_args()
	if os.path.exists(args.file):
		if args.file.endswith(".txt"):
			#实例化个对象
			_main = urlTrim(filename=args.file, retrieval=args.retrieval, cut_str=args.cut, move_str=args.move, scan=args.scan, f_add=args.fadd, e_add=args.eadd, conn_thread=args.thread)
			#运行main方法执行所选功能
			_main.main()
		else:
			print()
			print("[!] 只能处理TXT文件")
	else:
		print(f"""
[!] 文件不存在: +=> {args.file}
""")
