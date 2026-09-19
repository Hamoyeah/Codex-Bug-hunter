# Codex-Bug-hunter

OpenAI Codex에서 사용할 수 있는 버그바운티 및 웹 보안 점검용 Agent Skills 모음입니다.

정찰, 취약점 분류, 검증, 증거 정리, 보고서 작성 흐름을 `$bughunter` 하나로 실행할 수 있습니다.

> 본인이 소유했거나 명시적으로 허가받은 대상에서만 사용하세요.
> 수집 과정에서 새로 발견한 도메인은 자동으로 허용 범위에 포함되지 않습니다.

## 설치

### Windows PowerShell

```powershell
git clone https://github.com/Hamoyeah/Codex-Bug-hunter.git
cd Codex-Bug-hunter
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -CodexOnly
```

### macOS / Linux

```bash
git clone https://github.com/Hamoyeah/Codex-Bug-hunter.git
cd Codex-Bug-hunter
bash scripts/install.sh --codex-only
```

설치가 끝나면 Codex를 새로 시작하세요. 스킬은 `~/.agents/skills`에 설치됩니다.

## 사용법

```text
$bughunter recon example.com
$bughunter hunt example.com
$bughunter triage
$bughunter report
```

명령 대신 자연어로 요청해도 됩니다.

```text
example.com은 점검 허가를 받은 대상이야.
이 도메인 범위 안에서만 정찰하고 공격 표면을 우선순위별로 정리해줘.
```

## 포함된 기능

- 총 **84개 스킬**
- 이 중 **58개는 `hunt-*` 스킬**
- Codex용 `$bughunter` 워크플로 라우터
- 정찰 및 분류용 `cbh` CLI
- 재개 가능한 engagement engine
- 범위 검사와 검증 절차
- 선택적 Burp MCP 연동
- Claude Code 호환용 **15개 slash commands**

`subfinder`, `httpx`, `katana`, `gau`, Burp 등이 설치되어 있으면 더 넓게 수집하며,
없어도 기본 기능은 실행됩니다.

## CLI

```bash
pipx install git+https://github.com/Hamoyeah/Codex-Bug-hunter.git
```

```bash
cbh recon example.com
cbh surface example.com
cbh triage
```

## 문서

- [설치 안내](INSTALL.md)
- [사용 안내](USAGE.md)
- [스킬 목록](docs/skills.md)
- [CLI 안내](docs/cbh-cli.md)
- [보안 정책](SECURITY.md)

## 출처 및 라이선스

이 프로젝트는
[`elementalsouls/Claude-BugHunter`](https://github.com/elementalsouls/Claude-BugHunter)를
Codex에서 사용할 수 있도록 수정한 배포판입니다.

원본 저작자와 외부 자료에 대한 표기는 [`NOTICE`](NOTICE)와
[`docs/credits.md`](docs/credits.md)에 유지되어 있습니다.

- 소스 코드: [MIT](LICENSE)
- 문서 및 방법론 콘텐츠: [CC BY 4.0](LICENSE-CONTENT)
