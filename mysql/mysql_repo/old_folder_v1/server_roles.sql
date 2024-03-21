-- mysql server-roles
-- legacy impl: 'roles table'

CREATE TABLE server_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO server_roles (name) VALUES
    ('ROLE_UNVERIFIED_USER'),
    ('ROLE_USER'),
    ('ROLE_VERIFIED_USER'),
    ('ROLE_SUPER_USER'),
    ('ROLE_MOD_USER'),
    ('ROLE_MANAGER'),
    ('ROLE_ADMIN'),
    ('ROLE_SUPER_ADMIN');
