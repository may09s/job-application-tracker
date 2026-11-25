CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    position TEXT NOT NULL,
    date_applied TEXT NOT NULL,
    status TEXT NOT NULL,
    notes TEXT
);
