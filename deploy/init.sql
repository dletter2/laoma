-- Resource Share Site Database Initialization
-- Run this script to create tables and seed data

-- Tables are created by init_db.py automatically on first run.
-- This SQL script is for reference / manual setup.

-- Preset categories
INSERT OR IGNORE INTO categories (name, sort_order) VALUES
    ('教程资料', 1),
    ('软件工具', 2),
    ('模板素材', 3),
    ('文档报告', 4),
    ('设计资源', 5),
    ('其他', 6);

-- Default admin user (password: admin123, bcrypt hashed)
-- Run: python -m scripts.seed_data
-- This will create admin user with hashed password

-- Sample resources (optional, for testing)
-- INSERT INTO resources (title, summary, category_id, tags, file_size, uploader_id, status, is_hot)
-- VALUES ('示例资源', '这是一个测试资源', 1, '测试', 1024, 1, 'published', 1);
