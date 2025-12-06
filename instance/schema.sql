PRAGMA foreign_keys = ON;

-- =====================================
-- XÓA BẢNG NẾU ĐÃ TỒN TẠI (THEO THỨ TỰ PHỤ THUỘC)
-- =====================================
DROP TABLE IF EXISTS BAOTRI;
DROP TABLE IF EXISTS THONGBAO;
DROP TABLE IF EXISTS YEUCAUPHANANH;
DROP TABLE IF EXISTS CHISODIENNUOC;
DROP TABLE IF EXISTS LICHSUTHANHTOAN;
DROP TABLE IF EXISTS CHITIETDICHVU;
DROP TABLE IF EXISTS HOADON;
DROP TABLE IF EXISTS DICHVU;
DROP TABLE IF EXISTS DANGKYLuutru;
DROP TABLE IF EXISTS PHUONGTIEN;
DROP TABLE IF EXISTS LICHSUTHUE;
DROP TABLE IF EXISTS HOPDONG;
DROP TABLE IF EXISTS PHONG;
DROP TABLE IF EXISTS NHANVIEN;
DROP TABLE IF EXISTS KHACHTHUE;
DROP TABLE IF EXISTS TAIKHOAN;

-- =====================================
-- 1. BẢNG TÀI KHOẢN
-- =====================================
CREATE TABLE TAIKHOAN (
    MaTK        INTEGER PRIMARY KEY AUTOINCREMENT,
    TenDangNhap TEXT    NOT NULL UNIQUE,
    MatKhau     TEXT    NOT NULL,
    VaiTro      TEXT            -- admin / nhanvien / khach
);

-- =====================================
-- 2. KHÁCH THUÊ & NHÂN VIÊN
-- =====================================
CREATE TABLE KHACHTHUE (
    MaKT         INTEGER PRIMARY KEY AUTOINCREMENT,
    TenKT        TEXT    NOT NULL,
    SDT          TEXT,
    Email        TEXT,
    CCCD         TEXT,
    DiaChi       TEXT,
    NgayCheckin  TEXT,   -- 'YYYY-MM-DD'
    NgayCheckout TEXT,
    MaTK         INTEGER,
    FOREIGN KEY (MaTK) REFERENCES TAIKHOAN (MaTK)
);

CREATE TABLE NHANVIEN (
    MaNV   INTEGER PRIMARY KEY AUTOINCREMENT,
    TenNV  TEXT    NOT NULL,
    VaiTro TEXT,
    Email  TEXT,
    MaTK   INTEGER,
    FOREIGN KEY (MaTK) REFERENCES TAIKHOAN (MaTK)
);

-- Thêm sau bảng NHANVIEN là hợp lý
CREATE TABLE CHUNHA (
    MaCN   INTEGER PRIMARY KEY AUTOINCREMENT,
    TenCN  TEXT NOT NULL,
    SDT    TEXT,
    Email  TEXT,
    MaTK   INTEGER UNIQUE,
    FOREIGN KEY (MaTK) REFERENCES TAIKHOAN (MaTK)
);


-- =====================================
-- 3. PHÒNG, HỢP ĐỒNG, LỊCH SỬ THUÊ
-- =====================================
CREATE TABLE PHONG (
    MaPhong   INTEGER PRIMARY KEY AUTOINCREMENT,
    TenPhong  TEXT,
    DienTich  REAL,
    GiaThue   REAL,
    TrangThai TEXT,    -- TRONG / DANG_THUE / BAO_TRI ...
    TienIch   TEXT
);

CREATE TABLE HOPDONG (
    MaHD        INTEGER PRIMARY KEY AUTOINCREMENT,
    NgayBatDau  TEXT,
    NgayKetThuc TEXT,
    TrangThai   TEXT,
    TienCoc     REAL,
    MaKT        INTEGER NOT NULL,
    MaPhong     INTEGER NOT NULL,
    FOREIGN KEY (MaKT)    REFERENCES KHACHTHUE (MaKT),
    FOREIGN KEY (MaPhong) REFERENCES PHONG     (MaPhong)
);

CREATE TABLE LICHSUTHUE (
    MaLST       INTEGER PRIMARY KEY AUTOINCREMENT,
    NgayBatDau  TEXT,
    NgayKetThuc TEXT,
    TrangThai   TEXT,
    MaKT        INTEGER NOT NULL,
    MaPhong     INTEGER NOT NULL,
    MaHD        INTEGER NOT NULL,
    FOREIGN KEY (MaKT)    REFERENCES KHACHTHUE (MaKT),
    FOREIGN KEY (MaPhong) REFERENCES PHONG     (MaPhong),
    FOREIGN KEY (MaHD)    REFERENCES HOPDONG   (MaHD)
);

-- =====================================
-- 4. PHƯƠNG TIỆN & ĐĂNG KÝ LƯU TRÚ
-- =====================================
CREATE TABLE PHUONGTIEN (
    MaPT   INTEGER PRIMARY KEY AUTOINCREMENT,
    LoaiXe TEXT,
    BienSo TEXT,
    MauXe  TEXT,
    MaKT   INTEGER NOT NULL,
    FOREIGN KEY (MaKT) REFERENCES KHACHTHUE (MaKT)
);

CREATE TABLE DANGKYLuutru (
    MaDK        INTEGER PRIMARY KEY AUTOINCREMENT,
    NgayDangKy  TEXT,
    NgayHetHan  TEXT,
    MaKT        INTEGER NOT NULL,
    MaPhong     INTEGER NOT NULL,
    FOREIGN KEY (MaKT)    REFERENCES KHACHTHUE (MaKT),
    FOREIGN KEY (MaPhong) REFERENCES PHONG     (MaPhong)
);

-- =====================================
-- 5. DỊCH VỤ, HÓA ĐƠN, CHI TIẾT DV, LỊCH SỬ THANH TOÁN, CHỈ SỐ ĐIỆN NƯỚC
-- =====================================
CREATE TABLE DICHVU (
    MaDV   INTEGER PRIMARY KEY AUTOINCREMENT,
    TenDV  TEXT,
    DonGia REAL,
    LoaiDV TEXT
);

CREATE TABLE HOADON (
    MaHDon             INTEGER PRIMARY KEY AUTOINCREMENT,
    NgayTao            TEXT,
    TongTien           REAL,
    TrangThaiThanhToan TEXT,
    MaHD               INTEGER NOT NULL,
    FOREIGN KEY (MaHD) REFERENCES HOPDONG (MaHD)
);

CREATE TABLE CHITIETDICHVU (
    MaCT    INTEGER PRIMARY KEY AUTOINCREMENT,
    MaHDon  INTEGER NOT NULL,
    MaDV    INTEGER NOT NULL,
    SoLuong INTEGER,
    DonGia  REAL,
    FOREIGN KEY (MaHDon) REFERENCES HOADON (MaHDon),
    FOREIGN KEY (MaDV)   REFERENCES DICHVU (MaDV)
);

CREATE TABLE LICHSUTHANHTOAN (
    MaTT        INTEGER PRIMARY KEY AUTOINCREMENT,
    SoTien      REAL,
    NgayTT      TEXT,
    PhuongThucTT TEXT,
    MaHDon      INTEGER NOT NULL,
    FOREIGN KEY (MaHDon) REFERENCES HOADON (MaHDon)
);

CREATE TABLE CHISODIENNUOC (
    MaCS       INTEGER PRIMARY KEY AUTOINCREMENT,
    ChiSoDien  INTEGER,
    ChiSoNuoc  INTEGER,
    DonGiaDien REAL,
    DonGiaNuoc REAL,
    Thang      INTEGER,
    Nam        INTEGER,
    MaPhong    INTEGER NOT NULL,
    MaHDon     INTEGER,
    FOREIGN KEY (MaPhong) REFERENCES PHONG  (MaPhong),
    FOREIGN KEY (MaHDon)  REFERENCES HOADON (MaHDon)
);

-- =====================================
-- 6. YÊU CẦU / PHẢN ÁNH, THÔNG BÁO, BẢO TRÌ
-- =====================================
CREATE TABLE YEUCAUPHANANH (
    MaYC      INTEGER PRIMARY KEY AUTOINCREMENT,
    TieuDe    TEXT,
    NoiDung   TEXT,
    NgayGui   TEXT,
    TrangThai TEXT,
    MaKT      INTEGER NOT NULL,
    MaNV      INTEGER,
    FOREIGN KEY (MaKT) REFERENCES KHACHTHUE (MaKT),
    FOREIGN KEY (MaNV) REFERENCES NHANVIEN  (MaNV)
);

CREATE TABLE THONGBAO (
    MaTB      INTEGER PRIMARY KEY AUTOINCREMENT,
    NoiDung   TEXT,
    NgayGui   TEXT,
    TrangThai TEXT,
    MaKT      INTEGER,
    MaNV      INTEGER,
    FOREIGN KEY (MaKT) REFERENCES KHACHTHUE (MaKT),
    FOREIGN KEY (MaNV) REFERENCES NHANVIEN  (MaNV)
);

CREATE TABLE BAOTRI (
    MaBT       INTEGER PRIMARY KEY AUTOINCREMENT,
    NgayBaoTri TEXT,
    NoiDung    TEXT,
    ChiPhi     REAL,
    TrangThai  TEXT,
    MaPhong    INTEGER NOT NULL,
    MaNV       INTEGER,
    FOREIGN KEY (MaPhong) REFERENCES PHONG    (MaPhong),
    FOREIGN KEY (MaNV)    REFERENCES NHANVIEN (MaNV)
);
