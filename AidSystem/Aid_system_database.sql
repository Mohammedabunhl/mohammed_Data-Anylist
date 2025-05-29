CREATE TABLE IF NOT EXISTS beneficiaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_male VARCHAR(255) NOT NULL,
    name_female VARCHAR(255) ,
    national_id_1 VARCHAR(50) ,
    national_id_2 VARCHAR(50) ,
    phone_number VARCHAR(15) NOT NULL,
    family_members INT NOT NULL,
    family_members_injured INT NOT NULL,
    injured ENUM('نعم', 'لا') NOT NULL,
    damage_status ENUM('كلي', 'جزئي', 'غير متضرر') NOT NULL,
    aid_type VARCHAR(100) NOT NULL,
    aid_amount FLOAT DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    area VARCHAR(255),
    landmark VARCHAR(255),
    gender ENUM('ذكر', 'أنثى') NOT NULL DEFAULT 'ذكر',
    marital_status ENUM('أعزب', 'متزوج', 'مطلق', 'أرمل') NOT NULL DEFAULT 'أعزب',
    wives_count TINYINT DEFAULT 0,
    wife2_name VARCHAR(255),
    wife2_national_id VARCHAR(50),
    wife3_name VARCHAR(255),
    wife3_national_id VARCHAR(50),
    wife4_name VARCHAR(255),
    wife4_national_id VARCHAR(50),
    notes TEXT,
    other_type_help VARCHAR(255)
);
ALTER TABLE beneficiaries
ADD COLUMN Resident_displaced ENUM('مقيم', 'نازح') NOT NULL DEFAULT 'مقيم';

select *
from beneficiaries;
select *
from beneficiaries;
DESCRIBE beneficiaries;
ALTER TABLE beneficiaries
MODIFY COLUMN national_id_2 VARCHAR(50);
alter table beneficiaries
modify column name_female VARCHAR(255);

SELECT national_id_1, LENGTH(national_id_1) FROM beneficiaries WHERE national_id_1 LIKE '%41133713%';
SELECT * FROM beneficiaries WHERE TRIM(national_id_1) =41133713;
ALTER TABLE notifications ADD COLUMN is_read BOOLEAN DEFAULT 0;
select *
from notifications ;

describe notifications;

SHOW TABLES;
SHOW COLUMNS FROM beneficiaries;

CREATE TABLE donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donor_name VARCHAR(255),                -- اسم المتبرع
    contact VARCHAR(255),                   -- وسيلة التواصل
    aid_type VARCHAR(100) NOT NULL,         -- نوع المساعدة
    amount varchar(100),                  -- القيمة أو الكمية
    description TEXT,                       -- وصف إضافي
    beneficiary_national_id VARCHAR(50),    -- رقم هوية المستفيد
    status ENUM('تم', 'لم يتم') DEFAULT 'لم يتم', -- حالة التوزيع
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP -- تاريخ التسجيل
);
select *
from donations;

ALTER TABLE users
ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'viewer';

UPDATE users
SET role = 'admin'
WHERE username = 'admin';  -- غيّر الاسم حسب الموجود عندك


SELECT *
FROM users;
delete from users
where id=4;
select *
from notifications;
CREATE INDEX idx_national_id_1 ON beneficiaries(national_id_1);

CREATE TABLE IF NOT EXISTS requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    national_id_1 VARCHAR(50) NOT NULL,  -- مفتاح خارجي يربط المستفيد
    request_type VARCHAR(100) NOT NULL,  -- نوع الطلب (سلة غذاء، دواء، بطانية...)
    description TEXT,                    -- تفاصيل إضافية
    status ENUM('قيد الانتظار', 'قيد التنفيذ', 'تم التنفيذ', 'مرفوض') DEFAULT 'قيد الانتظار',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (national_id_1) REFERENCES beneficiaries(national_id_1)
        ON DELETE CASCADE
);


select *
from notifications;

CREATE TABLE children (
    id INT AUTO_INCREMENT PRIMARY KEY,
    beneficiary_id INT NOT NULL,
    name VARCHAR(255),
    national_id VARCHAR(50),
    birthdate DATE,
    FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries(id) ON DELETE CASCADE
);
ALTER TABLE users MODIFY password VARCHAR(255);
update users
set password='scrypt:32768:8:1$WicqGLPFXJvVzosk$ab68bd4382a4e6b633f9072e84158c4615b79b530a5b766a130bf356a26b35571a6366df1a15507a4033a8e065c82ddcfbff397a7cf8b344b2f22e3875de2060'
where username='admin';

select *
from notifications;


CREATE TABLE IF NOT EXISTS delete_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    beneficiary_id INT NOT NULL,
    requested_by VARCHAR(100) NOT NULL,          -- اسم المستخدم اللي طلب الحذف
    status ENUM('بانتظار', 'مقبول', 'مرفوض') DEFAULT 'بانتظار',
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    decision_date DATETIME DEFAULT NULL,
    decision_by VARCHAR(100) DEFAULT NULL,       -- اسم الأدمن اللي اتخذ القرار
    FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries(id) ON DELETE CASCADE
);
ALTER TABLE delete_requests
ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;
SELECT * FROM delete_requests;
