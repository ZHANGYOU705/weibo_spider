import os
import requests

api_url = "https://weibo.com/ajax/statuses/show?id=NhoHGkhwU&locale=zh-CN"
download_directory = "/Users/zhangyou/Disk_T_TestFile/weibo_spider"

try:
    response = requests.get(api_url, timeout=(10, 20))  # 连接超时5秒，读取超时10秒
    if response.status_code != 200:
        print("请求失败")
        exit(1)

    data = response.json()
    # 使用ID作为文件夹名
    folder_name = data['mblogid']
    folder_path = os.path.join(download_directory, folder_name)  # 设置文件夹的完整路径

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
