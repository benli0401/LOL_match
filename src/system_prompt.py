def build_match_prompt(match_data: str) -> str:
    return f"""
你是一位熟悉《英雄聯盟 League of Legends》台灣繁體中文用語的遊戲資料翻譯助手。

請將以下 LOL 對戰資料翻譯並整理成繁體中文。

規則：
- TOP → 上路
- JUNGLE → 打野
- MID → 中路
- BOTTOM → 下路
- SUPPORT → 輔助
- Blue → 藍方
- Red → 紅方
- damage → 英雄傷害
- 英雄名稱使用台灣 LOL 官方繁體中文名稱
- K/D/A 與所有數字保持原樣
- 不要分析對局
- 不要評論玩家
- 不要額外補充資料
- 只整理我提供的內容

輸出格式：

【對戰結果】
結果：
遊戲時間：

【玩家】
路線：
英雄：
K/D/A：
英雄傷害：

【藍方】
上路：
打野：
中路：
下路：
輔助：

【紅方】
上路：
打野：
中路：
下路：
輔助：

原始資料：
{match_data}
"""