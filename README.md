# 웹 추적 및 핑거프린팅 실험 프로젝트

이 프로젝트는 웹사이트에서 사용자 정보를 수집하는 방법과 보안 도구로 이를 차단하는 방법을 실증적으로 비교하는 실험용 애플리케이션입니다.

## 🎯 프로젝트 목표

1. **일반 사용자 환경**: 웹사이트가 수집할 수 있는 정보의 범위를 확인
2. **보안 사용자 환경**: Tor 브라우저와 JavaScript 차단으로 정보 수집을 막는 방법 확인
3. **비교 분석**: 두 환경의 차이를 통한 보안 도구의 효과성 검증

## 📋 기술 스택

- **Backend**: FastAPI (Python)
- **Database**: Firebase Firestore (선택사항, 로그 저장용)
- **Frontend**: HTML + JavaScript (Vanilla JS)
- **Deployment**: 로컬 서버 (무료 호스팅 가능)

## 🚀 설치 및 실행 방법

### 1. 프로젝트 클론 및 의존성 설치

```bash
# 가상 환경 생성 (권장)
python -m venv venv

# 가상 환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. Firebase 설정 (선택사항)

Firebase를 사용하지 않으면 터미널 로그만 출력됩니다.

#### Firebase 프로젝트 생성
1. [Firebase Console](https://console.firebase.google.com/)에 접속
2. 새 프로젝트 생성
3. 프로젝트 설정 > 서비스 계정으로 이동
4. "새 비공개 키 생성" 클릭하여 JSON 파일 다운로드
5. 다운로드한 파일을 `firebase-credentials.json`로 이름 변경
6. 프로젝트 루트 디렉토리에 저장

#### Firestore 데이터베이스 설정
1. Firebase Console에서 Firestore Database 생성
2. 테스트 모드로 시작 (개발 중에는 괜찮음)

### 3. 서버 실행

```bash
python main.py
```

서버가 시작되면 다음 주소에서 접속 가능합니다:
- 웹 페이지: http://127.0.0.1:8000
- API 문서: http://127.0.0.1:8000/docs

## 📊 수집되는 정보

### 수동적 정보 수집 (PASSIVE HEADERS)
서버에서 HTTP 요청 헤더에서 자동으로 수집:
- IP 주소
- User-Agent (브라우저 정보)
- Referer (이전 페이지)
- Accept-Language
- Accept-Encoding
- 기타 HTTP 헤더

### 능동적 핑거프린팅 (ACTIVE FINGERPRINT)
JavaScript로 수집되는 정보:
- 브라우저/OS 정보 (navigator.userAgent)
- 화면 해상도 (screen.width, screen.height)
- 시간대 (getTimezoneOffset)
- Canvas 핑거프린트 (고유한 그래픽 렌더링 값)
- WebGL 핑거프린트 (GPU 모델명 및 정보)
- 하드웨어 정보 (CPU 코어 수, 메모리 등)

### 활동 로깅 (ACTIVITY LOG)
사용자 상호작용 정보:
- 버튼 클릭 이벤트
- 스크롤 이벤트
- 타임스탬프
- 이벤트 발생 URL

## 🧪 실험 시나리오

### 시나리오 1: 일반 사용자 (대조군)
1. 일반 Chrome 브라우저로 http://127.0.0.1:8000 접속
2. "구매 버튼" 및 "광고 배너" 클릭
3. 서버 터미널에서 로그 확인
   - `[PASSIVE HEADERS]`: HTTP 헤더 정보
   - `[ACTIVE FINGERPRINT]`: 핑거프린트 정보
   - `[ACTIVITY LOG]`: 활동 로그

**예상 결과**: 모든 정보가 수집됨

### 시나리오 2: 보안 사용자 (실험군)
1. [Tor Browser](https://www.torproject.org/) 다운로드 및 설치
2. Tor 브라우저 설정에서 보안 수준을 "가장 안전함(Safest)"으로 설정
3. Tor 브라우저로 http://127.0.0.1:8000 접속
4. 버튼 클릭 시도

**예상 결과**: 
- `[PASSIVE HEADERS]`만 수집됨 (IP는 Tor 노드 IP, User-Agent는 표준화됨)
- `[ACTIVE FINGERPRINT]`와 `[ACTIVITY LOG]`는 JavaScript 차단으로 수집되지 않음

## 📁 프로젝트 구조

```
NewProject/
├── main.py                  # FastAPI 서버 (백엔드)
├── index.html              # 웹 페이지 (프론트엔드)
├── requirements.txt        # Python 의존성
├── .env.example           # 환경 변수 예시
├── .gitignore            # Git 무시 파일
├── README.md             # 프로젝트 설명서
└── firebase-credentials.json  # Firebase 인증 파일 (직접 생성)
```

## 🔍 로그 확인 방법

### 터미널 로그
서버 실행 중 터미널에서 실시간으로 확인 가능:
```
[2024-01-01 12:00:00] [PASSIVE HEADERS]
============================================================
{
  "ip_address": "127.0.0.1",
  "user_agent": "Mozilla/5.0...",
  ...
}
============================================================
```

### Firebase 로그 (Firebase 사용 시)
Firebase Console > Firestore Database에서 확인:
- `passive_headers` 컬렉션: 수동적 정보
- `fingerprints` 컬렉션: 핑거프린트 정보
- `activity_logs` 컬렉션: 활동 로그

## ⚙️ API 엔드포인트

- `GET /`: 메인 웹 페이지 (HTML 반환)
- `POST /api/fingerprint`: 핑거프린트 정보 수신
- `POST /api/log_event`: 활동 로그 수신

자세한 API 문서는 http://127.0.0.1:8000/docs 에서 확인할 수 있습니다.

## 🔒 보안 및 개인정보 보호

⚠️ **주의사항**:
- 이 프로젝트는 **교육 및 연구 목적**으로만 사용해야 합니다.
- 실제 사용자 데이터를 수집할 때는 법적 요구사항을 준수해야 합니다.
- Firebase 사용 시 보안 규칙을 적절히 설정하세요.
- 프로덕션 환경에서는 `.env` 파일과 `firebase-credentials.json`를 절대 공유하지 마세요.

## 📝 라이선스

이 프로젝트는 교육 목적으로 자유롭게 사용할 수 있습니다.

## 🐛 문제 해결

### 서버가 시작되지 않을 때
- 포트 8000이 이미 사용 중인지 확인
- `requirements.txt`의 모든 패키지가 설치되었는지 확인

### Firebase 연결 실패
- `firebase-credentials.json` 파일이 프로젝트 루트에 있는지 확인
- Firebase 프로젝트에서 Firestore가 활성화되어 있는지 확인
- 파일 권한이 올바른지 확인

### JavaScript가 실행되지 않을 때
- 브라우저 개발자 도구에서 콘솔 오류 확인
- JavaScript가 차단되어 있지 않은지 확인

## 📚 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Firebase 공식 문서](https://firebase.google.com/docs)
- [Tor Project](https://www.torproject.org/)
- [Canvas Fingerprinting](https://en.wikipedia.org/wiki/Canvas_fingerprinting)

