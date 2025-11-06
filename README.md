# Kcopa Chatbot

## 설명

- kcopa chatbot 구현을 위한 프로젝트.
- LLM 질문을 위한 pipeline을 구성하는 서버.

## 실행방법

```shell
$ uv run python -m app.main
```

- 원하는 모드에 맞게 아래와 같이 `value` 수정 후 위 커맨드 실행.

### REST API

- .env 내부 APP_MODE를 `api`로 수정

```
PROFILE=local
APP_MODE=api
PORT=8000
```

### UI

- .env 내부 APP_MODE를 `ui`로 수정

```
PROFILE=local
APP_MODE=ui
PORT=8000
```
