import os
from dotenv import load_dotenv
load_dotenv()
import openai
import twstock
import re


openai.api_key = os.getenv("OPENAI_API_KEY")

default_data = {
    "中油": "6505",
    "台積電": "2330",
    "鴻海": "2317",
    "台泥": "1101",
    "富邦金": "2881",
    "儒鴻": "1476",
    "技嘉": "2376",
    "潤泰全": "2915",
    "同欣電": "6271",
    "亞泥": "1102",
    "國泰金": "2882",
    "聚陽": "1477",
    "微星": "2377",
    "神基": "3005",
    "台表科": "6278",
    "統一": "1216",
    "玉山金": "2884",
    "東元": "1504",
    "台光電": "2383",
    "信邦": "3023",
    "啟碁": "6285",
    "台塑": "1301",
    "元大金": "2885",
    "華新": "1605",
    "群光": "2385",
    "欣興": "3037",
    "旭隼": "6409",
    "南亞": "1303",
    "兆豐金": "2886",
    "長興": "1717",
    "漢唐": "2404",
    "健鼎": "3044",
    "GIS-KY": "6456",
    "台化": "1326",
    "台新金": "2887",
    "台肥": "1722",
    "友達": "2409",
    "景碩": "3189",
    "愛普": "6531",
    "遠東新": "1402",
    "中信金": "2891",
    "台玻": "1802",
    "超豐": "2441",
    "緯創": "3231",
    "和潤企業": "6592",
    "亞德客-KY": "1590",
    "第一金": "2892",
    "永豐餘": "1907",
    "京元電子": "2449",
    "玉晶光": "3406",
    "富邦媒": "8454",
    "中鋼": "2002",
    "統一超": "2912",
    "大成鋼": "2027",
    "義隆": "2458",
    "創意": "3443",
    "億豐": "8464",
    "正新": "2105",
    "大立光": "3008",
    "上銀": "2049",
    "華新科": "2492",
    "群創": "3481",
    "寶成": "9904",
    "和泰車": "2207",
    "聯詠": "3034",
    "川湖": "2059",
    "興富發": "2542",
    "台勝科": "3532",
    "美利達": "9914",
    "聯電": "2303",
    "台灣大": "3045",
    "南港": "2101",
    "長榮": "2603",
    "嘉澤": "3533",
    "中保科": "9917",
    "台達電": "2308",
    "日月光投控": "3711",
    "裕隆": "2201",
    "裕民": "2606",
    "聯合再生": "3576",
    "巨大": "9921",
    "國巨": "2327",
    "遠傳": "4904",
    "裕日車": "2227",
    "陽明": "2609",
    "健策": "3653",
    "裕融": "9941",
    "台塑化": "6505",
    "聯強": "2347",
    "臺企銀": "2834",
    "臻鼎-KY": "4958",
    "南電": "8046",
    "佳世達": "2352",
    "遠東銀": "2845",
    "祥碩": "5269",
    "聯發科": "2454",
    "豐泰": "9910",
    "宏碁": "2353",
    "開發金": "2883",
    "遠雄": "5522",
    "可成": "2474",
    "大成": "1210",
    "鴻準": "2354",
    "新光金": "2888",
    "瑞儀": "6176",
    "台灣高鐵": "2633",
    "佳格": "1227",
    "英業達": "2356",
    "國票金": "2889",
    "聯茂": "6213",
    "彰銀": "2801",
    "聯華": "1229",
    "致茂": "2360",
    "永豐金": "2890",
    "力成": "6239"
}


def extract_stock_id(user_input: str) -> list:
    """
    從使用者輸入中提取股票代號。
    股票代號應為 4~6 位的數字。
    如果沒有找到，請求 OpenAI API 提取股票代號。
    """
    # 嘗試從使用者輸入中提取股票代號
    match = re.findall(r'\d{4,6}', user_input)
    if match:
        return match

    # 如果沒有找到，請求 OpenAI API 協助提取
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # 或其他你設定的模型
            messages=[
                {"role": "system", "content": "你是一個可以提取與辨識公司股票代號的助手。功能一：提取句子中的數字，或是，功能二：回答句子中提及的可辨識的公司的股票代號，只輸出純數字"},
                {"role": "user", "content": f"請從這段文字中提取股票代號或是依據內容回答提到的公司的股票代號：{user_input}，常見代碼：{default_data}；如果沒有找到與公司相關的股票資訊的話，回傳“None”"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        # 從 API 回應中提取文字
        ai_response = response.choices[0].message.content
        # print(f"OpenAI API response: {ai_response}")
        # test = [0]
        # test[0] = ai_response
        # return test  # 調試輸出
        match = re.findall(r'\d{4,6}', ai_response)
        return match if match else None
    except Exception as e:
        print(f"Error contacting OpenAI API: {e}")
        return None

def get_stock_info(stock_id: str) -> str:
    """
    查詢股票資訊，返回近五日數據。
    """
    try:
        stock = twstock.Stock(stock_id)
        recent_dates = stock.date[-30:]
        recent_prices = stock.price[-30:]
        recent_highs = stock.high[-30:]

        if None in recent_prices or None in recent_highs:
            return f"抱歉，無法取得 {stock_id} 的完整數據，請稍後再試。"

        result = f"股票代號：{stock_id}\n近五日數據：\n"
        for i in range(len(recent_dates)):
            date_str = recent_dates[i].strftime("%Y-%m-%d")
            result += f"- 日期：{date_str}，收盤價：{recent_prices[i]}，高點：{recent_highs[i]}\n"
        return result
    except Exception as e:
        return f"抱歉，無法取得股票代號 {stock_id} 的資訊。\n錯誤原因：{e}"

def process_user_input(user_input: str) -> str:
    """
    處理使用者輸入，執行股票查詢並交由 GPT 分析。
    """
    # 提取股票代號
    stock_id = extract_stock_id(user_input)
    # return stock_id[0] # 調試輸出
    if stock_id:
        # 查詢股票資訊
        stock_info = ''
        for sid in stock_id:
            stock_info += get_stock_info(sid) + '\n'
        # 傳遞股票資訊給 GPT 分析
        return chat_with_gpt(f"使用者輸入：{user_input}。以下是股票 {stock_id} 的資訊：\n{stock_info}\n。請先按照格式輸出資訊，再提供專業的分析或建議，並回答使用者問題。")
    else:
        # 若未偵測到股票代號，直接詢問 GPT
        return chat_with_gpt(user_input)

def chat_with_gpt(prompt: str) -> str:
    """
    與 GPT 互動，生成回應。
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一個使用繁體中文的聊天機器人，會回答股票相關的問題。若是沒有收到股票資訊，可以建議使用者透過股票代碼搜尋。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        return f"GPT API 錯誤: {e}"
    except Exception as e:
        return f"未知錯誤: {e}"