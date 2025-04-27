import json
import re
import requests

ENDPOINT = "http://localhost:11434/api/chat" # 本地模型endpoint


def query_ollama_chat(conversation, model_name="deepseek-llm"): # pull deepseek llm
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model_name,
                "messages": conversation,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        print("❌ Exception in query_ollama_chat:", str(e))
        return "[Local inference failed]"

#Create Prompt
system_prompt = """You are a flight assistant. Your job is to extract structured flight details from a user's message during a conversation.

✈️ You must collect and extract the following **exact fields**:
- Airline
- Origin → Only the city name (e.g., "Los Angeles", not airport name or state)
- Destination → Only the city name
- Month (1–12) → Return as a number only
- Day of Month (1–31) → Return as a number only
- Day of Week (1 = Monday to 7 = Sunday) → Return as a number only
- Schedule Departure Time (e.g., "8:15am")
- Schedule Arrival Time (e.g., "4:45pm")
- Actual Departure Time (e.g., "8:35am")

🧠 BEHAVIOR RULES:
1. Do **NOT** return a JSON object unless **all fields** above are clearly provided.
2. Ask follow-up questions to gather missing information — **one question per turn**.
3. **NEVER** make up, guess, or assume any information, including airport codes or times.
4. If user gives a city and airport together (e.g., “Los Angeles LAX”), extract only the **city name**.
5. Do **NOT** ask for or assume actual arrival time — you only need actual **departure** time.
6. If the user asks unrelated questions, politely ask them to describe their flight instead.
7. You must always check which fields are still missing. Ask about them one at a time until you have all 9 required fields.
8. If the user provides multiple fields in one sentence, extract all that you can from the input — do not wait to ask separately.
9. NEVER reuse or copy values from other fields (e.g., do NOT assume arrival time equals departure time). Only extract explicitly mentioned values.
🟢 Once all required fields are collected, respond with **ONLY a valid JSON object** using this exact format:

{
  "Airline": "Delta Airlines",
  "Origin": "Los Angeles",
  "Destination": "Boston",
  "Month": 3,
  "Day of Month": 26,
  "Day of Week": 2,
  "Schedule Departure Time": "8:15am",
  "Schedule Arrival Time": "4:45pm",
  "Actual Departure Time": "8:35am"
}

⚠️ NO explanation. NO extra messages. NO markdown. NO additional text. Just the JSON object."""


# create function to extract info

def extract_slots_loop(initial_input, conversation=None, collected_slots=None):
    required_fields = [
        "Airline", "Origin", "Destination", "Month", "Day of Month", "Day of Week",
        "Schedule Departure Time", "Schedule Arrival Time", "Actual Departure Time"
    ]
    
    # ✅ 初始化对话历史，确保 system prompt 存在
    if conversation is None:
        conversation = []
    if not any(m["role"] == "system" for m in conversation):
        conversation.insert(0, {"role": "system", "content": system_prompt})
    # ✅ 初始化已提取槽位信息
    if collected_slots is None:
        collected_slots = {}
    # ✅ 添加用户输入
    if collected_slots:
        missing_fields = [f for f in required_fields if collected_slots.get(f) in [None, "", 0]]
        if missing_fields:
            initial_input = f"(Missing fields: {', '.join(missing_fields)}) {initial_input}"
    
    conversation.append({"role": "user", "content": initial_input})

    # ✅ 获取 LLM 回复
    reply = query_ollama_chat(conversation).strip()
    print("🧠 Raw LLM Reply:\n", reply)

    # ✅ 添加 assistant 回复
    conversation.append({"role": "assistant", "content": reply})
    print("🧠 Current Collected Slots:", collected_slots)
    print("🧠 Full Assistant Reply:", reply)
    # ✅ 尝试提取 JSON
    # 尝试提取 JSON 块（完整字段集）
    match = re.search(r'\{[\s\S]*?\}', reply)
    # 映射别名或修正拼写， 防止llm输出和模型输入的匹配问题
            
    if match:
        try:
            slots = json.loads(match.group(0))
            alias_map = {
                "Scheduled Departure Time": "Schedule Departure Time",
                "Scheduled Arrival Time": "Schedule Arrival Time"
            }
            def get_standard_field_name(k):
                return alias_map.get(k.strip(), k.strip())
            
            for k, v in slots.items():
                if v not in [None, "", 0]:
                    std_key = get_standard_field_name(k)
                    collected_slots[std_key] = v
        except json.JSONDecodeError:
            print("❌ JSON parse error – invalid JSON block")

    # 否则使用关键词匹配进行增量提取（fallback 模式）
    else:
        for field in required_fields:
            pattern = rf'{field}:\s*["\']?([\w\s:]+)["\']?'  # 简单正则，匹配字段
            found = re.search(pattern, reply, re.IGNORECASE)
            if found:
                value = found.group(1).strip()
                if value and field not in collected_slots:
                    collected_slots[field] = value
    # ✅ 检查缺失字段
    missing_fields = [f for f in required_fields if collected_slots.get(f) in [None, "", 0]]
    return collected_slots, conversation, missing_fields
