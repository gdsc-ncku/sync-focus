# Sync Focus

> StayFocus but support sync browsing data across different device and browser

Sync Mind: 通過創新的用戶登錄系統, 提供了跨設備瀏覽數據的同步功能, 旨在為你所有的在線活動帶來前所未有的連貫性和便利性。配備了專為瀏覽器設計的追蹤庫和精巧的日志分析工具, 並結合GenAI, 讓使用者能夠洞察自己的網路使用習慣，優化時間管理。無論是開發者尋求提升生產力, 還是日常用戶想要更有效地管理在線時間, Sync Mind都是你專屬的提升工作效率、實現生活平衡的絕佳工具。

## API

登入目前暫時直接在前端生uuid, 然後每個請求都把 user uuid 帶進 query (如果 API endpoint 要求登入)

### 1. Heartbeat

#### 1-1. Send Heartbeat to Backend

> require login

- Request Method: POST
- Request Route: /heartbeat

- Request Body

`application/json`

|   Field    |   Type   |
|:----------:|:--------:|
|   domain   |   str    |
|    path    |   str    |
| user_agent |   str    |
|    time    | datetime |
|  browser   |   str    |

### 2. Usage

#### 2-1. User Usage by Time Range
>
> require login

- Request Method: GET
- Request Route: /usage

- Request Query

|    Field    |   Type    |
|:-----------:|:---------:|
| domain_list | List[str] |
| start_time  | datetime  |
|  end_time   | datetime  |

- Response

> return a mapping, key: 網站domain, value: 該使用者在查詢區間內的使用時間

| Field  |      Type      | Example                           |
|:------:|:--------------:| --------------------------------- |
| usages | Dict[str, int] | {{"a.com": 1}, {"b.com": 2}, ...} |

### 3. Summary

> for dashboard

#### 3-1. 列出使用者用過的domain
>
> require login

- Request Method: GET
- Request Route: /summaries/domain

- Request Query

| Field  | Type |
|:------:|:----:|
| offset | int  |
| limit  | int  |

- Response

> return a list of domain, orderd by latest visit domain

|  Field  |   Type    | Example            |
|:-------:|:---------:| ------------------ |
| domains | List[str] | ["a.com", "b.com"] |

#### 3-2. 使用者的特定domain使用情況 - 同個domain的每個路徑的使用時間(unit: sec)
>
> require login

- Request Method: GET
- Request Route: /summaries/path

- Request Query

| Field  | Type |
|:------:|:----:|
| domain | str  |

- Response

> return a mapping, key: path, value: path的使用時間

|  Field  |   Type    | Example            |
|:-------:|:---------:| ------------------ |
| usages | Dict[str, int] | {{"/meow": 1}, {"/cat": 2}, ...} |

#### 3-3. 使用者的特定domain使用情況 - 同個domain在不同的 user-agent 上的使用分佈(including browser type, host os, ...)
>
> require login

- Request Method: GET
- Request Route: /summaries/path

- Request Query

| Field  | Type |
|:------:|:----:|
| domain | str  |

- Response

> return a mapping, key: user-agent, value: user-agent的使用時間

|  Field  |   Type    | Example            |
|:-------:|:---------:| ------------------ |
| usages | Dict[str, int] | {{"Mozilla/5.0 (X11; Linux x86_64)": 1}, {"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)": 2}, ...} |

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
