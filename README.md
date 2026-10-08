# i can do it 자격증

ADsP(데이터분석 준전문가) 자격증 대비 퀴즈 앱. React Native(Expo) 클라이언트 + Express/tRPC 서버로 이루어진 모노레포다.

## 화면

<table>
  <tr>
    <td align="center"><img src="docs/screenshots/home.png" width="220" alt="홈: 시험 D-day·오늘의 목표"><br><sub>홈: 시험 D-day·오늘의 목표</sub></td>
    <td align="center"><img src="docs/screenshots/quiz-tab.png" width="220" alt="문제 풀기: 모의고사·과목별·기출"><br><sub>문제 풀기: 모의고사·과목별·기출</sub></td>
    <td align="center"><img src="docs/screenshots/question.png" width="220" alt="문제 풀이: 정답 확인 후 해설"><br><sub>문제 풀이: 정답 확인 후 해설</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/screenshots/result.png" width="220" alt="결과: 맞힌 문제까지 다시 보기"><br><sub>결과: 맞힌 문제까지 다시 보기</sub></td>
    <td align="center"><img src="docs/screenshots/dongurae-chalkboard.png" width="220" alt="동그래 칠판 해설"><br><sub>동그래 칠판 해설</sub></td>
    <td align="center"><img src="docs/screenshots/wrong-notes.png" width="220" alt="오답노트: 간격 반복 복습"><br><sub>오답노트: 간격 반복 복습</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/screenshots/stats.png" width="220" alt="학습 통계: 약한 과목 추천"><br><sub>학습 통계: 약한 과목 추천</sub></td>
    <td align="center"><img src="docs/screenshots/login.png" width="220" alt="로그인"><br><sub>로그인</sub></td>
    <td align="center"><img src="docs/screenshots/home-dark.png" width="220" alt="다크 모드"><br><sub>다크 모드</sub></td>
  </tr>
</table>

스크린샷은 `pnpm dev`를 켠 상태에서 `pnpm screenshots`로 다시 찍을 수 있다 ([`e2e/capture-readme.mts`](e2e/capture-readme.mts)).

## 기능

- **과목별 문제풀이**: 1과목(10문제)/2과목(10문제)/3과목(30문제) 또는 전체. 안 푼 문제 우선 출제, 약점 집중 모드 지원.
- **실전 모의고사**: 1과목 10 + 2과목 10 + 3과목 30 = 50문제, 90분 타이머. 매번 기출 복원 문제(data/past-exams.ts)에서 랜덤으로 다시 뽑고, 지난 회차를 다시 볼 수 있다. 타이머는 마감 시각 기준이라 앱이 백그라운드에 있어도 정확하고, 시간이 다 되면 자동 제출된다.
- **기출 회차**: 연도별·회차별로 묶어서 "연습"(한 문제씩 해설 확인) 또는 "⏱ 실전"(그 회차 그대로 90분 응시, 합격 판정, 회차별 최고 점수 표시)으로 푼다.
- **오답노트**: 틀린 문제를 간격 반복(spaced repetition)으로 복습 예정일에 다시 출제. 일반/기출 문제를 나눠 보고, 문제별 개인 메모 가능.
- **동그래 해설**: 틀린 문제를 마스코트 "동그래"가 설명해 준다. 해설은 고른 보기에 맞춰 AI(OpenAI)가 칠판 그림 장면으로 만들고, AI 목소리(OpenAI TTS)로 자막과 함께 읽어 준다. 아래 "AI 해설·목소리 캐시" 참고.
- **사진 인식(OCR)**: 문제 사진을 찍으면 AI가 문제/보기를 인식하고 해설까지 생성.
- **홈 / 학습 통계**: 오늘의 목표 카드, 연속 학습일(스트릭), 과목별 정답률(일반 문제 기준), 최근 7일 학습량 그래프.
- **북마크 / 검색**.
- **로그인과 내 정보**: 이메일/비밀번호, Google 로그인(서버를 거치는 브라우저 방식이라 Expo Go·아이폰·안드로이드 모두 동작), 이메일 인증코드 기반 비밀번호 찾기. "내 정보 수정"에서 닉네임·비밀번호 변경과 회원 탈퇴.
- **다크모드 / 글자 크기 조절** 등 개인화 설정.

AI 기능(사진 인식·해설·목소리)은 로그인한 사용자만 쓸 수 있다. AI 서버가 바쁘거나 연결이 끊기면 한 번 재시도하고, 그래도 안 되거나 요청 한도(429)에 걸리면 대체 모델로 넘어간 뒤, 끝내 실패하면 이유를 한국어로 안내한다 (`server/lib/ai.ts`).

### AI 해설·목소리 캐시

AI 호출은 쓴 만큼 돈이 들고 시간도 걸려서, 한 번 잘 만든 결과는 DB에 저장해 **모든 사용자가 같이 쓴다**.

- **해설** (`explanation_cache`): (문제, 고른 보기)마다 하나. 고른 보기가 다르면 해설도 다르다. 끝까지 정상 생성된 오답 해설만 저장한다.
- **칠판 대본** (`scene_cache`): (문제, 고른 보기)마다 하나.
- **목소리** (`speech_cache_v2`): 읽을 문장마다 하나 (목소리를 바꾸면 저장 키가 달라져 예전 음성은 쓰지 않는다). 메모리 → DB → 새로 생성 순으로 찾고, 끝까지 정상 생성된 음성만 저장한다. 처음 듣는 문장은 생성에 1분 안팎이 걸리고, 그동안 기다리는 시간이 표시된다. 100초 안에 음성이 준비되지 않거나, 받은 음성이 8초 안에 재생되지 않으면 폰 기본 목소리로 대신 읽는다(서버는 끝까지 만들어 저장하므로 다음부터는 AI 목소리).
- **미리 만들기** (기본 꺼짐): 실서버(`NODE_ENV=production` + 원격 `DATABASE_URL`)에 `TTS_PREWARM=1`을 주면 문제은행 기본 해설(931개)의 목소리를 2분에 하나씩 미리 만들어 둔다. 사용자가 목소리를 만드는 중이면 양보하고, 한도에 걸리면 1시간 쉰다. 진행 상황은 `GET /api/tts-status`(`ready`/`total`).

## 기술 스택

- **클라이언트**: Expo(React Native) + Expo Router(파일 기반 라우팅) + NativeWind
- **서버**: Express + tRPC (`server/`)
- **DB**: SQLite(`@libsql/client` + drizzle-orm) — 로컬은 파일(`local.db`), 배포 환경은 [Turso](https://turso.tech)
- **AI**: OpenAI API (`gpt-6-luna`로 사진 인식·해설·칠판 대본, `gpt-4o-mini-tts`로 해설 음성)
- **이메일**: [Brevo](https://brevo.com) 트랜잭션 이메일 API (비밀번호 찾기 인증코드 발송)

## 배포 구조

| 구성 요소 | 서비스 | 비고 |
|---|---|---|
| API 서버 | [Render](https://render.com) | `render.yaml` 블루프린트로 배포. 무료 플랜은 SMTP 포트가 막혀 있어 이메일은 반드시 HTTP API(Brevo)로 보내야 한다. |
| DB | [Turso](https://turso.tech) | `DATABASE_URL`(+`DATABASE_AUTH_TOKEN`)만 설정하면 코드 변경 없이 로컬 SQLite와 동일한 클라이언트로 붙는다. |
| Android 빌드 | [EAS Build](https://docs.expo.dev/build/introduction/) | 선택. 평소 테스트는 Expo Go로 충분하고, 설치형 APK가 필요할 때만 `eas.json` 프로필로 빌드한다. |
| Expo Go용 업데이트 | [EAS Update](https://docs.expo.dev/eas-update/introduction/) | 선택. PC(Metro) 없이 Expo Go로 앱을 열 때. 아래 "PC 없이 Expo Go로 열기" 참고. |

## 로컬에서 실행하기

```bash
pnpm install
cp .env.example .env   # 아래 "환경변수" 표를 참고해 채운다
pnpm dev                 # API 서버(3000) + Metro(8081) 동시 실행
```

- 웹 브라우저: `http://localhost:8081`
- 같은 와이파이의 실기기(Expo Go): `.env`의 `EXPO_PUBLIC_API_BASE_URL`을 이 컴퓨터의 LAN IP로 설정하고 QR 스캔
- 서버 단독 개발 가이드는 [`server/README.md`](server/README.md), 테스트 실행 방법은 [`TESTING.md`](TESTING.md) 참고

### PC 없이 Expo Go로 열기

Metro는 이 컴퓨터에서 도는 개발 서버라 PC가 꺼지면 앱도 못 연다. 현재 코드를 Expo 클라우드(EAS Update)에 올려 두면 PC 없이 Expo Go로 열 수 있다.

```bash
EXPO_GO_UPDATE=1 npx eas-cli update --branch expo-go --environment production --message "설명"
```

- `EXPO_GO_UPDATE=1`이면 런타임 버전이 Expo Go와 맞는 `exposdk:57.0.0`이 된다(`app.config.ts`). 설치형 빌드는 계속 `fingerprint` 정책을 쓴다.
- 올리면 나오는 Update group ID로 `exp://u.expo.dev/<프로젝트 ID>/group/<group ID>` 주소를 만들어 QR로 찍는다(`node scripts/generate_qr.mjs "<주소>"`). 올릴 때마다 group ID가 바뀌므로 QR도 새로 만든다.
- 배포 서버 주소 `EXPO_PUBLIC_API_BASE_URL`은 EAS 환경변수(production·preview·development)에 등록돼 있어서, `.env`가 없는 컴퓨터에서 올려도 Render 주소가 들어간다. `--environment`를 주면 EAS는 로컬 `.env`를 읽지 않으므로, 주소를 바꿀 때는 `npx eas-cli env:update`로 EAS 쪽 값을 고친다. 이 값이 빠지면 앱이 `localhost:3000`을 찾아 서버에 못 붙는다.
- Google 로그인은 서버가 `exp://u.expo.dev/<우리 프로젝트 ID>/...`로의 복귀만 허용한다.

### 환경변수

`.env.example`에 전체 목록과 설명이 있다. 필수/선택 요약:

| 변수 | 필수 여부 | 설명 |
|---|---|---|
| `OPENAI_API_KEY` | 필수 | 사진 인식·해설·칠판 대본·동그래 목소리. https://platform.openai.com/api-keys |
| `JWT_SECRET` | 배포 시 필수 | 로그인 토큰 서명 키. 비우면 개발용 기본값 사용. |
| `DATABASE_URL` / `DATABASE_AUTH_TOKEN` | 선택 | 비우면 로컬 `local.db` 사용. Turso 같은 원격 DB로 옮길 때만 채운다. |
| `GOOGLE_WEB_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Google 로그인 쓸 때만 | Google Cloud Console "웹 애플리케이션" OAuth 클라이언트의 ID와 보안 비밀번호. 리디렉션 URI에 `https://<API 서버>/api/auth/google/callback` 등록 필요. |
| `EXPO_RETURN_HOSTS` | ngrok 등 외부 터널로 Expo Go 쓸 때만 | Google 로그인 후 돌아갈 수 있는 개발 서버 호스트(쉼표 구분). 같은 와이파이 주소는 자동 허용. |
| `BREVO_API_KEY` / `BREVO_SENDER_EMAIL` | 비밀번호 찾기 쓸 때만 | Brevo API 키와 발신자 인증을 마친 이메일 주소. |
| `EXPO_PUBLIC_API_BASE_URL` | 실기기 테스트 시 필수 | 앱이 API 서버를 찾을 주소. |
| `TTS_PREWARM` | 선택 | `0`이면 실서버의 동그래 목소리 미리 만들기를 끈다. |

## 배포하기

1. **DB**: Turso에 DB를 만들고 `DATABASE_URL`/`DATABASE_AUTH_TOKEN` 발급 (`drizzle-kit`이 `dialect: "turso"`로 자동 전환되므로 코드 수정 불필요).
2. **API 서버**: Render에서 이 저장소로 "New → Blueprint" 생성 → `render.yaml`이 빌드/시작 명령을 자동 설정 → 대시보드에서 위 환경변수 입력.
3. **Google 로그인**: Google Cloud Console에서 "웹 애플리케이션" OAuth 클라이언트 발급 → 승인된 리디렉션 URI에 `https://<API 서버>/api/auth/google/callback` 추가 → 클라이언트 ID/보안 비밀번호를 서버 환경변수로 입력. 앱은 인앱 브라우저로 서버를 거쳐 로그인하므로 네이티브 빌드가 필요 없다.
4. **비밀번호 찾기**: Brevo 가입 → API 키 발급 → 발신자 이메일 인증(도메인 인증 불필요, 단일 발신자 인증만으로 모든 수신자에게 발송 가능).
