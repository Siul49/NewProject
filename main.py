"""
FastAPI 서버 - 웹 추적 및 핑거프린팅 실험용
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from datetime import datetime
from typing import Dict, Any
import os

# Firebase 관련 (선택적)
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_ENABLED = True
except ImportError:
    FIREBASE_ENABLED = False
    print("⚠️ Firebase가 설치되지 않았습니다. 터미널 로그만 사용됩니다.")

app = FastAPI(title="웹 추적 실험 서버")

# CORS 설정 (로컬 개발용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase 초기화 (설정 파일이 있는 경우)
db = None
if FIREBASE_ENABLED:
    try:
        # Firebase 서비스 계정 키 파일 경로
        cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("✅ Firebase 연결 성공")
        else:
            print(f"⚠️ Firebase 인증 파일({cred_path})을 찾을 수 없습니다. 터미널 로그만 사용됩니다.")
    except Exception as e:
        print(f"⚠️ Firebase 초기화 실패: {e}. 터미널 로그만 사용됩니다.")

def log_to_console(tag: str, data: Dict[Any, Any], request: Request = None):
    """터미널에 로그 출력"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] [{tag}]")
    print("=" * 60)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("=" * 60)

def save_to_firestore(collection: str, data: Dict[Any, Any]):
    """Firebase Firestore에 데이터 저장"""
    if db is None:
        return
    try:
        data["timestamp"] = firestore.SERVER_TIMESTAMP
        db.collection(collection).add(data)
        print(f"💾 Firebase에 저장됨: {collection}")
    except Exception as e:
        print(f"❌ Firebase 저장 실패: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    메인 페이지 - 정적 HTML 파일 서빙
    서버에 자동으로 포함된 HTTP 헤더 정보 수집 및 로깅
    """
    # 수동적 정보 수집: HTTP 헤더에서 정보 추출
    client_host = request.client.host if request.client else "unknown"
    headers_dict = dict(request.headers)
    
    passive_data = {
        "ip_address": client_host,
        "user_agent": headers_dict.get("user-agent", "unknown"),
        "referer": headers_dict.get("referer", "none"),
        "accept_language": headers_dict.get("accept-language", "unknown"),
        "accept_encoding": headers_dict.get("accept-encoding", "unknown"),
        "connection": headers_dict.get("connection", "unknown"),
        "all_headers": headers_dict
    }
    
    # 터미널 로그 출력
    log_to_console("PASSIVE HEADERS", passive_data, request)
    
    # Firebase에 저장
    save_to_firestore("passive_headers", passive_data)
    
    # HTML 파일 반환
    html_path = "index.html"
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        return HTMLResponse(
            content="<h1>index.html 파일을 찾을 수 없습니다.</h1>",
            status_code=404
        )

@app.post("/api/fingerprint")
async def receive_fingerprint(request: Request):
    """
    API 엔드포인트 1: 핑거프린트 정보 수신
    페이지 로드 시 클라이언트에서 한 번 호출됨
    """
    try:
        data = await request.json()
        
        # 클라이언트 IP 추가
        client_host = request.client.host if request.client else "unknown"
        data["client_ip"] = client_host
        
        # 터미널 로그 출력
        log_to_console("ACTIVE FINGERPRINT", data, request)
        
        # Firebase에 저장
        save_to_firestore("fingerprints", data)
        
        return {"status": "success", "message": "핑거프린트 정보가 수신되었습니다."}
    except Exception as e:
        print(f"❌ 핑거프린트 수신 오류: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/log_event")
async def receive_log_event(request: Request):
    """
    API 엔드포인트 2: 활동 로그 수신
    사용자의 클릭/스크롤 등의 활동 시 호출됨
    """
    try:
        data = await request.json()
        
        # 클라이언트 IP 추가
        client_host = request.client.host if request.client else "unknown"
        data["client_ip"] = client_host
        
        # 터미널 로그 출력
        log_to_console("ACTIVITY LOG", data, request)
        
        # Firebase에 저장
        save_to_firestore("activity_logs", data)
        
        return {"status": "success", "message": "활동 로그가 수신되었습니다."}
    except Exception as e:
        print(f"❌ 활동 로그 수신 오류: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/api/behavior_pattern")
async def receive_behavior_pattern(request: Request):
    """
    API 엔드포인트 3: 행동 패턴 수신
    마우스 움직임 패턴, 키보드 타이핑 패턴 등 행동 생체인식 데이터 수신
    """
    try:
        data = await request.json()
        
        # 클라이언트 IP 추가
        client_host = request.client.host if request.client else "unknown"
        data["client_ip"] = client_host
        
        # 터미널 로그 출력
        pattern_type = data.get("type", "unknown")
        log_to_console(f"BEHAVIOR PATTERN ({pattern_type})", data, request)
        
        # Firebase에 저장
        save_to_firestore("behavior_patterns", data)
        
        return {"status": "success", "message": f"{pattern_type} 패턴이 수신되었습니다."}
    except Exception as e:
        print(f"❌ 행동 패턴 수신 오류: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 웹 추적 실험 서버 시작")
    print("=" * 60)
    print("📍 서버 주소: http://127.0.0.1:8000")
    print("📖 API 문서: http://127.0.0.1:8000/docs")
    print("=" * 60 + "\n")
    
    # reload 옵션을 사용하려면 import string 형식으로 전달해야 함
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

