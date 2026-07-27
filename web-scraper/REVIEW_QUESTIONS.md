# Bộ Câu Hỏi Review Dự Án Web Scraper (Boot.dev)

Tài liệu này chứa các câu hỏi ôn tập và thử thách giúp bạn củng cố kiến thức về **Python Asyncio**, **Web Scraping**, **HTTP Protocols**, và **Code Best Practices** sau khi hoàn thành dự án `web-scraper`.

---

## 📋 Nhóm 1: Bất đồng bộ & Xử lý đồng thời (Asyncio & Concurrency)

### 1. `asyncio.Lock` vs `asyncio.Semaphore`

- Trong [`AsyncCrawler`](async_crawler.py), dự án dùng cả `self.lock` và `self.semaphore`.
- **Câu hỏi:**
    1. `asyncio.Lock` có nhiệm vụ gì trong hàm `add_page_visit()` và khi ghi dữ liệu vào `self.page_data`?
        > Về cơ bản lock để tránh khi dùng shared state, gây ra race condition ghi sai dữ liệu do có nhiều request đồng thời, sai logic, unexpected behavior khi state bất ổn định
    2. `asyncio.Semaphore` đóng vai trò gì khi gọi `get_html()`?
        > Limit request đồng thời, đẩy vào queue tránh đụng rate limit
    3. Tại sao không thể dùng chung một loại lock cho cả 2 tác vụ trên?
        > 2 cái cho 2 case khác nhau nên không thể dùng chung

### 2. Concurrency vs Parallelism & GIL trong Python

- Khi chạy crawler với `max_concurrency = 10`, Python đang chạy dưới dạng **multi-threading**, **multi-processing** hay **single-threaded event loop**?
    > Single-threaded event loop. Python sử dụng 1 thread duy nhất để điều phối các coroutine thông qua vòng lặp sự kiện (Event Loop).
- **Câu hỏi:**
    1. GIL (Global Interpreter Lock) có ngăn cản `asyncio` tăng tốc độ cào web không? Tại sao?
        > Không. Vì cào web là tác vụ I/O-bound (dành hầu hết thời gian chờ đợi phản hồi từ mạng). Trong lúc chờ I/O (`await`), asyncio tự động nhường CPU cho các request khác trên cùng 1 thread, do đó GIL không trở thành điểm nghẽn.
    2. Sự khác biệt giữa I/O-bound task (như gửi HTTP request) và CPU-bound task (như tính toán ma trận) trong context của `asyncio` là gì?
        > - **I/O-bound task:** Dành phần lớn thời gian chờ tài nguyên bên ngoài. Khi gặp `await`, task tự nguyện nhường CPU cho Event Loop xử lý task khác, giúp chạy đồng thời (concurrency) rất hiệu quả.
        > - **CPU-bound task:** Đòi hỏi CPU tính toán liên tục. Nếu chạy trực tiếp trên Event Loop, nó sẽ chặn (block) thread duy nhất đó, làm tất cả các async task khác bị treo.

### 3. Gom nhóm Task & Xử lý ngoại lệ với `asyncio.gather`

- Trong `crawl_page()`, đoạn code gom nhóm task như sau:
    ```python
    await asyncio.gather(*tasks, return_exceptions=True)
    ```
- **Câu hỏi:**
  1. Tham số `return_exceptions=True` có ý nghĩa gì?
     > Giúp coi các lỗi (Exceptions) như những kết quả trả về bình thường thay vì quăng lỗi làm dừng chương trình. Danh sách trả về từ `gather` sẽ chứa cả dữ liệu cào thành công lẫn các đối tượng Exception của những URL bị lỗi.
  2. Nếu không đặt `return_exceptions=True` và 1 URL trong danh sách bị lỗi kết nối (Timeout/DNS fail), chuyện gì sẽ xảy ra với các URL khác đang chạy song song trong cùng đợt `gather`?
     > Lỗi (Exception) sẽ lập tức bị raise ra ngoài ngay tại dòng `await gather`, làm ngắt luồng thực thi chính. Các task còn lại vẫn chạy ngầm trong background nhưng kết quả của chúng sẽ bị bỏ rơi và không thể thu thập được.

### 4. Async Context Manager (`__aenter__` & `__aexit__`)

- Lớp `AsyncCrawler` triển khai `async with AsyncCrawler(...) as crawler:`
- **Câu hỏi:**
    1. Việc tạo duy nhất một `aiohttp.ClientSession` trong `__aenter__` mang lại lợi ích gì về mặt hiệu năng (Connection Pooling, Keep-Alive) so với việc tạo mới `ClientSession` mỗi lần fetch HTML?
    2. Chuyện gì xảy ra nếu chương trình bị crash giữa chừng? `__aexit__` giúp giải quyết vấn đề quản lý tài nguyên như thế nào?

---

## 🌐 Nhóm 2: Web Scraping & Chuẩn hóa dữ liệu (HTTP & Parsing)

### 5. Chuẩn hóa URL (URL Normalization)

- Hàm `normalize_url(url)` trong [`crawl.py`](crawl.py) thực hiện:
    ```python
    u = urlsplit(url)
    return u.netloc + u.path
    ```
- **Câu hỏi:**
    1. Giả sử trang web chứa các liên kết: `https://example.com/blog/`, `http://example.com/blog`, và `https://example.com/blog?tag=python`. Hàm trên sẽ normalize thành gì?
    2. Rủi ro của việc không loại bỏ trailing slash (`/` ở cuối) hoặc không xử lý Query Parameters / Anchor Hash (`#section`) là gì?

### 6. Giới hạn Domain (Same-Domain Policy)

- Đoạn code kiểm tra domain:
    ```python
    if url_split.netloc != self.base_domain:
        return
    ```
- **Câu hỏi:**
    1. Nếu `base_url` truyền vào là `https://blog.boot.dev`, `self.base_domain` sẽ là gì?
    2. Nếu crawler gặp đường dẫn tới `https://boot.dev` hoặc `https://sub.blog.boot.dev`, crawler có tiếp tục cào không? Làm thế nào để hỗ trợ hoặc chặn subdomain theo mong muốn?

---

## 🔍 Nhóm 3: Code Review, Edge Cases & Best Practices

### 7. Quản lý tài nguyên File trong `json_report.py`

- Hàm ghi file hiện tại:
    ```python
    f = open(filename, "w", encoding="utf-8")
    json.dump(pages, f, indent=2)
    ```
- **Câu hỏi:**
    1. Tại sao cách mở file trên chưa an toàn (nguy cơ Resource Leak khi xảy ra exception trong lúc `json.dump`)?
    2. Hãy viết lại hàm này sử dụng context manager `with open(...)` chuẩn Pythonic.

### 8. Kiểm tra điều kiện giới hạn `max_pages`

- Trong `add_page_visit()`:
    ```python
    if len(self.page_data) > self.max_pages:
        self.should_stop = True
    ```
- **Câu hỏi:**
    1. Nếu `max_pages = 5`, khi `len(self.page_data)` đạt 5, điều kiện `> 5` là `False`, nên trang thứ 6 vẫn có thể được chấp nhận. Điều kiện này nên sửa thành `>` hay `>=`?
    2. Do tính chất bất đồng bộ, nhiều task có thể cùng vượt qua bước `add_page_visit` trước khi `page_data` được cập nhật. Bạn sẽ tối ưu logic kiểm tra số lượng trang cào được như thế nào để đảm bảo chính xác không cào lố `max_pages`?

---

## 🚀 Nhóm 4: Bài tập thử thách nâng cấp dự án (Extra Challenges)

- [ ] **Thử thách 1:** Viết lại `json_report.py` dùng `with open(...) as f:` và sắp xếp các trang theo tiêu đề (heading) thay vì URL.
- [ ] **Thử thách 2:** Bổ sung xử lý retry (thử lại 3 lần) cho hàm `get_html()` khi gặp lỗi HTTP 5xx hoặc Timeout.
- [ ] **Thử thách 3:** Xử lý loại bỏ trailing slash `/` ở cuối `path` trong `normalize_url()`.
- [ ] **Thử thách 4:** Thêm tiến trình hiển thị (ProgressBar hoặc log số trang đã cào được/tổng số tối đa) realtime trong console khi crawler đang chạy.
