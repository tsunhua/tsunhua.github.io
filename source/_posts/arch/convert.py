import re
import os

def convert_format_a_to_b(text_a: str) -> str:
    """
    將格式 A 轉換成格式 B。
    處理兩種情況：帶超連結的來源和純文字來源。
    """
    # 移除首尾可能的多餘空白
    text_a = text_a.strip()
    
    # 如果是空行，直接返回空字串
    if not text_a:
        return ""

    # --- 規則 1: 處理帶有超連結的來源 ([來源](URL)) ---
    # 匹配 "圖：" 後的內容 (.*?)
    # 匹配來源標籤 ([來源])
    # 匹配 URL (URL)
    pattern_link = re.compile(
        r"圖：(.*?)（\[來源\]\((.*?)\)）$"
    )

    match_link = pattern_link.match(text_a)

    if match_link:
        content = match_link.group(1).strip()
        url = match_link.group(2).strip()
        # 構造格式 B：<center>圖：...<a href="...">（來源）</a></center>
        return f"<center>圖：{content}<a href=\"{url}\">（來源）</a></center>"

    # --- 規則 2: 處理純文字來源 (來源：文字) ---
    # 匹配以 "圖：" 開頭，以 "(來源：...)" 結尾的行
    pattern_text_source = re.compile(
        r"圖：(.*?)（來源：.*?）$"
    )

    if pattern_text_source.match(text_a):
        # 找到第一個 "圖：" 後的字串（包含內容和來源）
        # 由於內容和來源部分都是我們想要的，直接提取並加上 <center> 標籤
        content_and_source = text_a.split('圖：', 1)[1].strip()
        # 構造格式 B：<center>圖：...（來源：...）</center>
        return f"<center>圖：{content_and_source}</center>"
        
    # 如果沒有匹配任何預期格式，返回原始行（或加上錯誤標記，這裡選擇返回原始行）
    return text_a
    

def process_file(input_filename: str, output_filename: str):
    """
    讀取輸入檔案，逐行轉換格式，並寫入輸出檔案。
    """
    try:
        # 1. 讀取輸入檔案
        with open(input_filename, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

    except FileNotFoundError:
        print(f"錯誤：找不到輸入檔案 '{input_filename}'。請確認檔案是否存在。")
        return
    except Exception as e:
        print(f"讀取檔案時發生錯誤：{e}")
        return

    # 2. 處理並轉換每一行
    converted_lines = []
    print(f"開始處理 {len(lines)} 行...")
    
    for i, line in enumerate(lines, 1):
        # 呼叫轉換函數
        converted_line = convert_format_a_to_b(line)
        converted_lines.append(converted_line)
        
        # 保持與原始檔案的換行符一致
        if converted_line and converted_line.strip():
             converted_lines.append("\n")
        elif not converted_line:
             converted_lines.append("\n")


    # 3. 寫入輸出檔案
    try:
        # 為了避免連續換行，我們將轉換後的結果（不帶額外換行符）連接起來，
        # 並且只在非空行後添加換行符。
        # 上一步已經處理了換行，這裡使用 'w' 模式寫入整個列表。
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            # 寫入前先過濾掉空的元素，然後再寫入
            final_content = "".join([s for s in converted_lines if s is not None])
            outfile.write(final_content)
        
        print("-" * 30)
        print(f"處理完成！轉換後的內容已成功寫入檔案：'{output_filename}'")
        print(f"輸入檔案：'{input_filename}'")
        print(f"輸出檔案路徑：{os.path.abspath(output_filename)}")

    except Exception as e:
        print(f"寫入檔案時發生錯誤：{e}")

# --- 主程式執行區塊 ---
if __name__ == "__main__":
    # 您可以在這裡更改輸入和輸出的檔案名稱
    INPUT_FILE = "birds-eye-view-of-ancient-chinese-architecture-ii.md"
    OUTPUT_FILE = "birds-eye-view-of-ancient-chinese-architecture-ii-converted.md"
    
    process_file(INPUT_FILE, OUTPUT_FILE)