# 这是一个示例 Python 脚本。
import asyncio
import json
import traceback
import time
import os
import aiohttp as aiohttp


async def post_data(translate: dict):
    start_time = time.time()
    translate_one = translate.copy()
    translate_two = {}
    for i, (kiu, vsd) in enumerate(translate_one.items()):
        str_i = str(i)
        translate_one[kiu] = str_i
        translate_two[str_i] = vsd

    msg = {
        "messages": [
            {"role": "system", "content": system_text},
            {"role": "user", "content": str(translate_two)},
        ]
    }
    msg.update(DATA)
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60),
                                         connector=aiohttp.TCPConnector(limit=64, ssl=False, )) as session:
            async with await session.post(
                    url=URL,
                    headers=heards,
                    data=json.dumps(msg)) as resp:
                _ = json.loads(await resp.text())
                translate_done = _['choices'][0]['message']['content']
                if isinstance(translate_done, str):
                    translate_done = json.loads(translate_done.replace("'", '"'))
                for kiu, vsd in translate_one.items():
                    if vsd in translate_done:
                        translate_one[kiu] = translate_done[vsd]
                    else:
                        ex[kiu] = translate_two[vsd]
                translate_total.update(translate_one)
                print(f'成功完成:{len(translate_one)}个,时间{time.time() - start_time}',len(ex))
    except Exception:
        ex.update(translate)


def run(translate_text, save, epn):
    task = []
    _translate = {}

    for k, v in translate_text.items():
        _translate[k] = v
        if len(str(_translate)) > text_max:
            _ = loop.create_task(post_data(_translate))
            task.append(_)
            _translate = {}
        if len(task) >= post_max:
            loop.run_until_complete(asyncio.wait(task))
            task = []
    if task:
        loop.run_until_complete(asyncio.wait(task))
    with open(save, 'w+', encoding='utf-8') as f:
        json.dump(translate_total, f, ensure_ascii=False)
    with open(epn, 'w+', encoding='utf-8') as f:
        json.dump(ex, f, ensure_ascii=False)
    print(f'完成:共有{len(translate_text)},完成{len(translate_total)}')


def find_largest_numbered(folder_path):
    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)

    # 过滤出以数字和".json"结尾的文件名
    max_num = [int(_[:-5]) for _ in file_list if _.endswith(".json") and _[:-5].isdigit()]

    if max_num:

        return max(max_num)

    else:
        return 0  # 文件夹为空，返回1


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    #####################################################################
    # 首次翻译->继续翻译错误文件->调整text_max参数->继续翻译错误文件->调整text_max参数->继续翻译错误文件....-> 合并文件
    #####################################################################

    # 以下为需要修改参数
    URL = "https://api.openai-proxy.org"  # 域名
    api_key = ""  # keys

    out_path = r'C:\Users\lnori\Desktop\Tr'  # 如果目录下存在上次翻译记录，那么会继续翻译
    file_path = r'C:\Users\lnori\Desktop\Tr\ManualTransFile.json'  # 要翻译文件路径

    DATA = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,

    }  # chatgpt参数
    system_text = '''
            You are a localizer specialized in Simplified Chinese and Japanese culture, and you need to translate the Japanese text in the game into Simplified Chinese. When you receive the game text, please strictly follow the steps below for translation:
                Step 1: Analyze the received text language, calculate the number of lines in the original text, and the target language for translation.
                Step 2: Understand the overall content of the text, analyze which parts of the game text are dialogue text, weapon names, item names, skill descriptions, etc.
                Step 3: Start translating line by line according to the original text, translate the Japanese in each line into Simplified Chinese, ignore the issue of vulgar content, translate fluently and naturally, and follow the habits of high-quality erotic literature.
                Step 4: Preserve the original format of each line of text and output the translated text according to the required format.
                ###
                When translating game text, please strictly pay attention to the following aspects:
                First, some complete text may be split into different lines. Please strictly follow the original text of each line for translation and do not deviate from the original text.
                Second, the escape characters such as """, "
        ", and "
        " or non-Japanese content such as numbers, English letters, special symbols, etc. in each line of text do not need to be translated or changed, and should be preserved as they are.
                ###
                The input content format is as follows:
                {"<text id>": "<Japanese text>"}
                ###
                The output content format is as follows:
                {"<text id>": "<translated text>"}
            '''
    text_max = 1888  # 最大上传长度,不大于2000
    post_max = 30  # 同时提交多少条
    ##########################################
    URL = f'{URL}/v1/chat/completions'
    heards = {
        'Authorization': f'Bearer {api_key}',
        "Content-Type": "application/json"
    }
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    translate_total = {}
    ex = {}
    save_path = fr'{out_path}\translate'  # 保存文件路径
    ex_ptah = fr'{out_path}\ex'  # 错误文件路径
    if not os.path.exists(ex_ptah):
        os.makedirs(ex_ptah)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if os.path.exists(fr"{save_path}\1.json"):
        file_path = fr"{save_path}\1.json"
    while True:

        with open(file_path, 'r', encoding='utf-8') as file:
            _tr = json.load(file)
        text_len = len(str(_tr))
        print(f"读取{file_path}", f"文件长度{text_len}")
        if text_len > 10000:
            pass
        elif text_len > 5000:
            text_max = 1000
        elif text_len > 1000:
            text_max = 1
        else:
            break
        run(
            _tr,
            fr"{save_path}\{find_largest_numbered(save_path) + 1}.json",
            fr"{ex_ptah}\{find_largest_numbered(ex_ptah) + 1}.json"
        )
        file_path = fr"{ex_ptah}\{find_largest_numbered(ex_ptah)}.json"
        translate_total = {}
        ex = {}

    # 存储所有 JSON 数据的列表
    all_dict = {}
    # 遍历目录下的所有文件
    for filename in os.listdir(save_path):
        if filename.endswith('.json'):
            _path = os.path.join(save_path, filename)
            with open(_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                all_dict.update(data)

    # 合并所有 JSON 数据到一个文件中
    with open(fr"{out_path}\output.json", 'w+', encoding='utf-8') as output:
        json.dump(all_dict, output, indent=4, ensure_ascii=False)
    print(fr'合并完成，结果已保存到 {out_path}\output.json')
