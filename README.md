# Luxury-Apartment

Dự án cuối kỳ môn Phân tích & Thiết kế Yêu cầu.

## Run nhanh
```bash
pip install -r requirements.txt
python init_db.py
python run.py
```

## Cấu trúc code (bài bản)
- `src/` : toàn bộ backend code theo hướng App Factory + module hóa
  - `src/route/` : các route theo nhóm chức năng (Blueprint)
  - `src/model/` : dữ liệu/model (demo/DTO…)
  - `src/form/` : validate/handle input (để mở rộng)
  - `src/extensions/` : DB, extensions dùng chung
  - `src/utils/` : helper & decorators tái sử dụng
- `app/templates/` : HTML templates (giữ nguyên)
- `static/` : static assets
- `instance/` : schema SQL
- `legacy_app.py` : bản app.py cũ (monolith) để tham khảo

## Ghi chú
- Các URL giữ nguyên như trước: `/login`, `/iot/*`, `/reports/*`, `/admin/*`, ...
- `init_db.py` sẽ chạy cả `schema.sql` và `schema_iot.sql`.
