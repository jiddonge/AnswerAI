from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import csv
import os
from datetime import datetime
from fastapi.responses import JSONResponse

app = FastAPI()

# 로그 데이터 모델
class LogData(BaseModel):
    session_id: str
    사용자유형: str
    선택항목: str
    추천정책: str
    추천날짜: str  # YYYY-MM-DD
    정책최종수정일: str  # YYYY-MM-DD

# 로그를 CSV 파일에 저장하는 함수
def save_to_csv(log_data, file_path='chat_log.csv'):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=log_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_data)

# POST 요청 처리 (GPT Webhook)
@app.post("/log")
async def log_handler(data: LogData):
    log_dict = data.dict()
    save_to_csv(log_dict)
    print("✅ Webhook 수신됨:", log_dict)
    return {"message": "로그 저장 완료"}

# GET 요청 대응 (브라우저 접속 안내)
@app.get("/log")
async def log_get():
    return JSONResponse(
        content={"message": "이 경로는 POST 요청(Webhook 전용)입니다. 브라우저로는 사용하지 마세요."},
        status_code=200
    )

# 홈 경로에 안내 메시지
@app.get("/")
def home():
    return {"message": "답정너AI Webhook 서버가 실행 중입니다 ✅"}
