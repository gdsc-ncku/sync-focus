# Sync Mind

> StayFocus but support sync browsing data across different deivce and browser

## Cross device stay-focus

### 跨裝置 (支援登入)

- 1. 登入base: 寫一個網站讓使用者登入後產生token然後貼到extension的設定頁面
  - google login

### 範例

- [User behavior logging](https://github.com/susravan/User-behavior-logging)
  - chrome extension and backend had finished

- [user behaviour js lib](https://github.com/TA3/web-user-behaviour)
  - JS Library for user behaviour tracking from the browser, using mouse movements, clicks, scroll, and time on page.

## Log analyzer

### waka-time

>coding time visualizer

golang + postgres

- <https://github.com/muety/wakapi>

demo 範例

![image](https://hackmd.io/_uploads/BybcMvtO6.png)

## Collaboration

- [notion](https://www.notion.so/invite/67d9145b86eb7dcbd5a197547d617e4693a8ab16)

## Development

> python version: 3.11

```bash
poetry install
poetry shell
cp .env.example .env
docker compose up -d
make revision MESSAGE=init
make migrate
make run # run server
```

## Branch/Commit Type

- feat: 新增/修改功能 (feature)。
- fix: 修補 bug (bug fix)。
- docs: 文件 (documentation)。
- style: 格式 (不影響程式碼運行的變動 white-space, formatting, missing semicolons, etc.)。
- refactor: 重構 (既不是新增功能，也不是修補 bug 的程式碼變動)。
- perf: 改善效能 (A code change that improves performance)。
- test: 增加測試 (when adding missing tests)。
- chore: 建構程序或輔助工具的變動 (maintain)。
- revert: 撤銷回覆先前的 commit
