import os
import requests
from urllib.parse import urlparse


def download_weibo_content(share_url):
    try:
        # 解析分享链接获取微博ID
        url_components = urlparse(share_url)
        path_components = url_components.path.split('/')
        share_id = path_components[-1]

        if not share_id:
            print("无法从分享链接中获取微博ID")
            return

        api_url = f"https://weibo.com/ajax/statuses/show?id={share_id}&locale=zh-CN"

        response = requests.get(api_url, timeout=(10, 20))  # 连接超时5秒，读取超时10秒
        if response.status_code != 200:
            print("请求失败")
            return

        data = response.json()
        # 使用ID作为文件夹名
        user_name = data['user']['screen_name']
        folder_name = data['mblogid']
        if user_name is None or folder_name is None:
            print("未能获取用户名或文件夹名")
            return

        download_directory = "/Users/zhangyou/Disk_T_TestFile/weibo_spider"
        folder_path = os.path.join(download_directory, user_name, folder_name)  # 设置文件夹的完整路径

        # 1. 将文本内容输出到文件
        if 'text_raw' in data:
            text_raw = data['text_raw']
            os.makedirs(folder_path, exist_ok=True)  # 创建文件夹
            text_file_name = os.path.join(folder_path, f"{folder_name}.txt")
            with open(text_file_name, 'w', encoding='utf-8') as text_file:
                text_raw = text_raw.replace("​​​", "")
                text_file.write(text_raw)

            print("文本内容已保存到文件：", text_file_name)

        # 2. 下载图片并保存到文件
        pic_infos = data.get('pic_infos', [])
        for idx, pic_id in enumerate(data.get('pic_ids', [])):
            img_url = pic_infos[pic_id].get('original', {}).get('url', '')
            if not img_url:
                continue
            response = requests.get(img_url)
            if response.status_code == 200:
                img_data = response.content
                img_file_name = os.path.join(folder_path, f"img_{idx + 1}.jpg")
                with open(img_file_name, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"图片 {idx + 1} 已保存到文件：{img_file_name}")
            else:
                print(f"无法下载图片 {idx + 1}，HTTP错误码：{response.status_code}")

    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == '__main__':
    # share_url = "https://weibo.com/3975771323/Njepnbx7z"
    share_url = input("请输入你从微博分享的内容：")
    download_weibo_content(share_url)
