CREATE DATABASE ANTARANGA;
USE ANTARANGA;

CREATE TABLE locations(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255) NOT NULL,
nature_score INT,
adventure_score INT,
culture_score INT,
altitude_score INT
);

INSERT INTO locations (name, nature_score, adventure_score, culture_score, altitude_score) VALUES
('Everest Base Camp', 10, 10, 4, 10),
('Pokhara (Lakeside)', 9, 7, 5, 3),
('Kathmandu Durbar Square', 2, 2, 10, 4),
('Chitwan National Park', 10, 6, 6, 1),
('Lumbini (Birthplace of Buddha)', 6, 2, 10, 1),
('Annapurna Base Camp', 10, 9, 3, 9),
('Bhaktapur Durbar Square', 1, 1, 10, 4),
('Nagarkot (Sunrise View)', 8, 3, 4, 5),
('Rara Lake', 10, 8, 3, 5),
('Muktinath Temple', 7, 7, 9, 4),
('Ghorepani Poon Hill', 9, 7, 5, 7),
('Janakpur (Janaki Temple)', 4, 1, 10, 1),
('Bandipur Village', 7, 3, 8, 4),
('Langtang Valley', 9, 8, 6, 7),
('Manaslu Circuit', 10, 10, 5, 9),
('Ilam (Tea Gardens)', 9, 3, 4, 3),
('Upper Mustang (Lo Manthang)', 8, 9, 10, 4),
('Gosaikunda Lake', 9, 8, 7, 9),
('Patan Durbar Square', 2, 2, 10, 4),
('Bardia National Park', 10, 7, 5, 1);

USE ANTARANGA;
ALTER TABLE locations ADD COLUMN cluster_id INT NULL;
SELECT * FROM locations;