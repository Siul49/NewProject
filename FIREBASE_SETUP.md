# Firebase 설정 가이드

Firebase를 사용하여 로그를 저장하는 방법을 안내합니다. Firebase는 무료 플랜을 제공하며, 개발 및 테스트 용도로 충분합니다.

## 1단계: Firebase 프로젝트 생성

1. [Firebase Console](https://console.firebase.google.com/)에 접속
2. "프로젝트 추가" 클릭
3. 프로젝트 이름 입력 (예: "web-tracking-experiment")
4. Google Analytics 설정은 선택사항 (비활성화 가능)
5. "프로젝트 만들기" 클릭

## 2단계: Firestore 데이터베이스 활성화

1. Firebase Console 좌측 메뉴에서 "Firestore Database" 클릭
2. "데이터베이스 만들기" 클릭
3. "테스트 모드에서 시작" 선택 (개발 중에는 이렇게 하면 됨)
   - 프로덕션 환경에서는 보안 규칙을 설정해야 합니다
4. 위치 선택 (가장 가까운 리전 선택, 예: asia-northeast3)
5. "사용 설정" 클릭

## 3단계: 서비스 계정 키 생성

1. Firebase Console 우측 상단의 프로젝트 설정 아이콘 클릭
2. "프로젝트 설정" 선택
3. "서비스 계정" 탭으로 이동
4. "새 비공개 키 생성" 버튼 클릭
5. "키 생성" 확인
6. JSON 파일이 자동으로 다운로드됩니다

## 4단계: 인증 파일 설정

1. 다운로드한 JSON 파일을 프로젝트 루트 디렉토리로 이동
2. 파일 이름을 `firebase-credentials.json`로 변경
3. 파일이 `.gitignore`에 포함되어 있는지 확인 (보안을 위해 중요!)

## 5단계: 환경 변수 설정 (선택사항)

`.env` 파일을 생성하고 다음 내용 추가:
```
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
```

또는 파일이 프로젝트 루트에 있고 이름이 `firebase-credentials.json`이면 환경 변수 설정 없이도 작동합니다.

## 6단계: 서버 실행 및 확인

1. 서버를 실행합니다:
   ```bash
   python main.py
   ```

2. 서버 시작 시 다음과 같은 메시지가 표시되어야 합니다:
   ```
   ✅ Firebase 연결 성공
   ```

3. 웹 페이지에 접속하고 활동을 수행하면:
   - 터미널에 로그가 출력되고
   - Firebase Firestore에 데이터가 저장됩니다

## Firebase Console에서 데이터 확인

1. Firebase Console > Firestore Database로 이동
2. 다음 컬렉션에서 데이터를 확인할 수 있습니다:
   - `passive_headers`: HTTP 헤더 정보
   - `fingerprints`: 핑거프린트 정보
   - `activity_logs`: 활동 로그

## 무료 플랜 제한

Firebase 무료 플랜 (Spark)의 주요 제한:
- Firestore 읽기: 50,000건/일
- Firestore 쓰기: 20,000건/일
- 저장 용량: 1GB

실험 용도로는 충분합니다!

## 보안 규칙 설정 (프로덕션용)

프로덕션 환경에서는 Firestore 보안 규칙을 설정해야 합니다:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // 모든 접근 허용 (개발용만, 실제로는 인증 추가 필요)
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

실제 운영 시에는 인증을 추가하여 승인된 사용자만 접근할 수 있도록 해야 합니다.

