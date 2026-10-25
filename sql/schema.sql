CREATE TABLE users (
    id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username      VARCHAR(50)  NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('admin','kasir') NOT NULL,
    aktif         BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE paket (
    id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nama       VARCHAR(50)  NOT NULL,
    durasi_jam INT UNSIGNED NOT NULL,
    harga      INT UNSIGNED NOT NULL,
    aktif      BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tanpa kolom status: status dihitung dari waktu_kedaluwarsa (BR-03).
CREATE TABLE voucher (
    id               INT UNSIGNED NOT NULL AUTO_INCREMENT,
    kode             VARCHAR(16)  NOT NULL,
    paket_id         INT UNSIGNED NOT NULL,
    kasir_id         INT UNSIGNED NOT NULL,
    waktu_beli       DATETIME     NOT NULL,
    waktu_kedaluwarsa DATETIME    NOT NULL,
    created_at       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_voucher_kode (kode),
    KEY idx_voucher_waktu_beli (waktu_beli),
    CONSTRAINT fk_voucher_paket FOREIGN KEY (paket_id) REFERENCES paket(id),
    CONSTRAINT fk_voucher_kasir FOREIGN KEY (kasir_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Log pemakaian, bukan sesi aktif (BR-05, BR-07).
CREATE TABLE sesi_voucher (
    id           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    voucher_id   INT UNSIGNED NOT NULL,
    ip_address   VARCHAR(45)  NOT NULL,
    user_agent   VARCHAR(255) NULL,
    validated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_sesi_validated_at (validated_at),
    CONSTRAINT fk_sesi_voucher FOREIGN KEY (voucher_id) REFERENCES voucher(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
