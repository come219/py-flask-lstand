-- mysql server-info


CREATE TABLE server_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    members TINYINT,
    api VARCHAR(255),
    version VARCHAR(255),
    location VARCHAR(255),
    timezone VARCHAR(255),
    server_time DATETIME,
    game_time DATETIME,
	player_count INT,
	max_player_count INT,
	total_player_count INT,
	network_ping VARCHAR(255),
	network_packet VARCHAR(255)
	);

-- should implement id not to be auto incremement so that it can be managed better?

-- server type? - master, prod, test, 

--         ?ip?
--         ?load_balancer_ip?

--         network_ping, network_packet - call an api to get ping, packet