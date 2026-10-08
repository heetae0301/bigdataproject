# 테스트 실행 방법

이 프로젝트는 [Vitest](https://vitest.dev)로 테스트를 작성합니다. 테스트 파일은 [`__tests__/`](__tests__) 폴더에 있습니다.

## 1. pnpm 설치

이 프로젝트는 `pnpm@9.12.0`을 사용합니다 (`package.json`의 `packageManager` 필드). 아직 설치되어 있지 않다면 아래 중 하나로 설치하세요.

```
npm install -g pnpm@9.12.0
```

또는 (Node의 corepack이 정상 동작하는 환경이라면)

```
corepack enable
corepack prepare pnpm@9.12.0 --activate
```

## 2. 의존성 설치

```
cd adsp-quiz-app
pnpm install
```

## 3. 환경변수 설정 (선택)

단위 테스트는 AI를 가짜로 바꿔서 돌기 때문에 API 키가 없어도 모두 통과합니다.

`__tests__/openai-connection.test.ts`만 실제 OpenAI API를 부릅니다(호출마다 요금이 나감). 평소에는 건너뛰고, 키를 바꿨을 때만 `.env`에 `OPENAI_API_KEY`를 채운 뒤 아래처럼 돌립니다.

```
RUN_AI_LIVE=1 pnpm test __tests__/openai-connection.test.ts
```

## 4. 테스트 실행

전체 테스트 실행:

```
pnpm test
```

특정 파일만 실행:

```
pnpm test __tests__/storage.test.ts
```

## 참고: 확인된 실행 결과

API 키 없이 실행한 결과 (2026-10-07 기준): 115개 통과, 3개 건너뜀(`openai-connection` 실제 호출 테스트).

## 화면 테스트 (E2E)

[`e2e/`](e2e) 폴더의 테스트는 웹 앱을 실제 브라우저로 열어 버튼을 눌러 가며 확인합니다. 회원가입부터 문제 풀이, 결과 화면, 오답노트, 통계, 설정, 동그래 해설 플레이어, 칠판 해설, 오프라인일 때 로그인 유지까지 다룹니다.

1. 서버 두 개를 켭니다 (다른 터미널에서 켜 둔 채로 둡니다).

   ```
   pnpm dev
   ```

2. 테스트를 실행합니다.

   ```
   pnpm test:e2e                 # 전체 (약 15분)
   pnpm test:e2e player scenes   # 파일 이름에 들어간 단어로 일부만
   ```

알아 둘 점:

- **브라우저는 따로 받지 않습니다.** 설치된 Edge(Windows)나 Chrome(그 밖)을 씁니다. 다른 브라우저는 `E2E_BROWSER_CHANNEL=chrome` 또는 `E2E_BROWSER_PATH=<실행 파일 경로>`로 지정하고, 창을 띄워 보려면 `E2E_HEADED=1`을 붙입니다.
- **배포 DB는 건드리지 않습니다.** `.env`에 배포 서버 주소가 있어도 앱의 API 요청을 로컬 API(`localhost:3000`, `local.db`)로 돌립니다. 테스트할 때마다 `e2e+…@example.com` 계정이 `local.db`에 생깁니다.
- **AI 요금이 나가지 않습니다.** AI 해설·칠판 대본·AI 목소리 요청은 모두 가짜 응답으로 바꿉니다. 그래서 실제 AI가 만든 내용이 잘 나오는지는 폰에서 직접 확인해야 합니다.
- 실패하면 그 순간의 화면이 `e2e/shots/`에 저장됩니다 (git에는 올라가지 않음).
- 서버 주소를 바꾸려면 `E2E_APP_URL`, `E2E_API_URL`을 지정합니다.
