import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. 모델 ID 지정
MODEL_ID = "LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct"

# 2. 토크나이저 로드
# trust_remote_code=True는 EXAONE 모델의 커스텀 코드를 실행하는 데 필요할 수 있습니다.
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)

# 3. 모델 로드
# 2.4B 모델은 비교적 작지만, GPU 가속을 위해 device_map="auto"와 적절한 dtype을 사용합니다.
# 2.4B 모델은 BF16(bfloat16) 대신 FP16(float16)을 사용할 수도 있습니다.
# (대부분의 소비자용 GPU는 FP16에 더 익숙할 수 있습니다.)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,  # 또는 torch.bfloat16 (하드웨어 지원 시)
    trust_remote_code=True,
    device_map="auto" # 사용 가능한 GPU에 자동으로 로드 (작은 모델이라도 권장)
)

print(f"모델 '{MODEL_ID}' 로드 완료. 추론 준비 완료.")

# --- 예시 사용법 (선택 사항) ---
prompt = "커리어 디자인을 시작할 때 가장 먼저 해야 할 일은 무엇인가요?"
messages = [
    {"role": "system", "content": "당신은 사용자에게 전문적인 커리어 디자인을 도와주는 친절한 챗봇입니다."},
    {"role": "user", "content": prompt}
]

# EXAONE 모델은 apply_chat_template을 사용하여 프롬프트 형식을 지정하는 것을 권장합니다.
input_ids = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device) # GPU로 이동

output = model.generate(
    input_ids,
    max_new_tokens=256,
    do_sample=True,
    temperature=0.7,
    pad_token_id=tokenizer.eos_token_id  # 패딩 토큰 설정
)

response = tokenizer.decode(output[0, input_ids.shape[-1]:], skip_special_tokens=True)
print("\n[챗봇 응답]:")
print(response)