-- =====================================
-- SCHEMA CHO HỆ THỐNG IOT & NĂNG LƯỢNG
-- =====================================

-- Bảng thiết bị IoT
CREATE TABLE IF NOT EXISTS IOT_THIETBI (
    MaThietBi     INTEGER PRIMARY KEY AUTOINCREMENT,
    DeviceID      TEXT    NOT NULL UNIQUE,  -- ESP32-E001, WF-S001, etc
    TenThietBi    TEXT    NOT NULL,
    LoaiThietBi   TEXT    NOT NULL,         -- electric, water, temp, switch, lock
    MaPhong       INTEGER,
    IPAddress     TEXT,
    MACAddress    TEXT,
    TrangThai     TEXT    DEFAULT 'offline', -- online, offline, error
    NgayLapDat    TEXT,
    MoTa          TEXT,
    FOREIGN KEY (MaPhong) REFERENCES PHONG (MaPhong)
);

-- Bảng dữ liệu cảm biến (readings)
CREATE TABLE IF NOT EXISTS IOT_DULIEU (
    MaDuLieu      INTEGER PRIMARY KEY AUTOINCREMENT,
    MaThietBi     INTEGER NOT NULL,
    LoaiDuLieu    TEXT    NOT NULL,         -- electric, water, temperature, humidity
    GiaTri        REAL    NOT NULL,          -- Giá trị đo được
    DonVi         TEXT,                      -- kWh, m³, °C, %
    ThoiGian      TEXT    NOT NULL,          -- Timestamp
    FOREIGN KEY (MaThietBi) REFERENCES IOT_THIETBI (MaThietBi)
);

-- Bảng cảnh báo IoT
CREATE TABLE IF NOT EXISTS IOT_CANHBAO (
    MaCanhBao     INTEGER PRIMARY KEY AUTOINCREMENT,
    AlertID       TEXT    NOT NULL UNIQUE,  -- ALT-001, ALT-002
    LoaiCanhBao   TEXT    NOT NULL,         -- leak, overconsumption, device_offline, anomaly
    MucDo         TEXT    NOT NULL,         -- critical, warning, info
    TieuDe        TEXT    NOT NULL,
    NoiDung       TEXT,
    MaPhong       INTEGER,
    MaThietBi     INTEGER,
    ThoiGianPhatHien TEXT NOT NULL,
    ThoiGianGiaiQuyet TEXT,
    TrangThai     TEXT    DEFAULT 'new',   -- new, inprogress, resolved, dismissed
    NguoiXuLy     INTEGER,
    GhiChu        TEXT,
    FOREIGN KEY (MaPhong) REFERENCES PHONG (MaPhong),
    FOREIGN KEY (MaThietBi) REFERENCES IOT_THIETBI (MaThietBi),
    FOREIGN KEY (NguoiXuLy) REFERENCES NHANVIEN (MaNV)
);

-- Bảng quy tắc cảnh báo
CREATE TABLE IF NOT EXISTS IOT_QUYTUACCANHBAO (
    MaQuyTac      INTEGER PRIMARY KEY AUTOINCREMENT,
    TenQuyTac     TEXT    NOT NULL,
    LoaiThietBi   TEXT    NOT NULL,         -- electric, water, device
    DieuKien      TEXT    NOT NULL,         -- JSON: {"operator": ">", "value": 50, "unit": "kWh"}
    MucDo         TEXT    NOT NULL,         -- critical, warning, info
    HanhDong      TEXT,                      -- JSON: actions to take
    TrangThai     TEXT    DEFAULT 'active', -- active, paused
    NgayTao       TEXT,
    NguoiTao      INTEGER,
    FOREIGN KEY (NguoiTao) REFERENCES NHANVIEN (MaNV)
);

-- Bảng lịch sử điều khiển thiết bị
CREATE TABLE IF NOT EXISTS IOT_LICHSUDIEUKHIEN (
    MaLichSu      INTEGER PRIMARY KEY AUTOINCREMENT,
    MaThietBi     INTEGER NOT NULL,
    Lenh          TEXT    NOT NULL,         -- turn_on, turn_off, reset, lock_valve
    ThoiGian      TEXT    NOT NULL,
    NguoiThucHien INTEGER,
    KetQua        TEXT,                      -- success, failed
    GhiChu        TEXT,
    FOREIGN KEY (MaThietBi) REFERENCES IOT_THIETBI (MaThietBi),
    FOREIGN KEY (NguoiThucHien) REFERENCES TAIKHOAN (MaTK)
);

-- Bảng cấu hình ngưỡng cảnh báo theo phòng
CREATE TABLE IF NOT EXISTS IOT_NGUONGCANHBAO (
    MaNguong      INTEGER PRIMARY KEY AUTOINCREMENT,
    MaPhong       INTEGER NOT NULL,
    LoaiNangLuong TEXT    NOT NULL,         -- electric, water
    NgưỡngNgay    REAL,                      -- Ngưỡng tiêu thụ/ngày
    NgưỡngThang   REAL,                      -- Ngưỡng tiêu thụ/tháng
    PhaTramTangMax REAL,                     -- % tăng tối đa so với kỳ trước
    TrangThai     TEXT    DEFAULT 'active',
    FOREIGN KEY (MaPhong) REFERENCES PHONG (MaPhong)
);

-- Insert dữ liệu mẫu

-- Thiết bị IoT
INSERT INTO IOT_THIETBI (DeviceID, TenThietBi, LoaiThietBi, MaPhong, TrangThai, NgayLapDat) VALUES
('ESP32-E001', 'Cảm biến điện #01', 'electric', 1, 'online', '2024-01-15'),
('WF-S001', 'Cảm biến nước #01', 'water', 1, 'online', '2024-01-15'),
('ESP32-E042', 'Cảm biến điện #42', 'electric', 2, 'offline', '2024-02-20'),
('DHT22-T001', 'Cảm biến nhiệt độ #01', 'temp', 1, 'online', '2024-01-20'),
('SW-001', 'Công tắc thông minh #01', 'switch', 1, 'online', '2024-03-10'),
('WF-S015', 'Cảm biến nước #15', 'water', 2, 'error', '2024-01-25');

-- Quy tắc cảnh báo
INSERT INTO IOT_QUYTUACCANHBAO (TenQuyTac, LoaiThietBi, DieuKien, MucDo, TrangThai, NgayTao) VALUES
('Phát hiện rò rỉ nước', 'water', '{"operator":">","value":2,"unit":"m³/h","duration":5}', 'critical', 'active', '2024-01-01'),
('Tiêu thụ điện vượt ngưỡng', 'electric', '{"operator":">","value":50,"unit":"kWh/day"}', 'warning', 'active', '2024-01-01'),
('Thiết bị mất kết nối', 'device', '{"operator":"offline","duration":15}', 'critical', 'active', '2024-01-01');

-- Cảnh báo mẫu
INSERT INTO IOT_CANHBAO (AlertID, LoaiCanhBao, MucDo, TieuDe, NoiDung, MaPhong, MaThietBi, ThoiGianPhatHien, TrangThai) VALUES
('ALT-001', 'leak', 'critical', 'Phát hiện rò rỉ nước - Phòng 302', 'Lưu lượng nước bất thường: 2.5 m³/h', 2, 6, '2025-12-07 09:55:00', 'new'),
('ALT-002', 'device_offline', 'critical', 'Thiết bị mất kết nối - Cảm biến điện #42', 'Không phản hồi từ 30 phút trước', 2, 3, '2025-12-07 09:30:00', 'inprogress'),
('ALT-003', 'overconsumption', 'critical', 'Tiêu thụ điện vượt ngưỡng - Phòng 205', 'Tiêu thụ 85 kWh vượt ngưỡng 50 kWh', 1, 1, '2025-12-07 09:45:00', 'new');

-- Ngưỡng cảnh báo theo phòng
INSERT INTO IOT_NGUONGCANHBAO (MaPhong, LoaiNangLuong, NgưỡngNgay, NgưỡngThang, PhaThamTangMax, TrangThai) VALUES
(1, 'electric', 5, 140, 20, 'active'),
(1, 'water', 0.5, 15, 25, 'active'),
(2, 'electric', 5, 140, 20, 'active'),
(2, 'water', 0.5, 15, 25, 'active');