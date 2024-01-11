
-- mysql insert
INSERT INTO server_info (
    name,
    api,
	members,
    version,
    location,
    timezone,
    server_time,
    game_time,
    player_count,
    max_player_count,
    total_player_count,
    network_ping,
    network_packet
) VALUES (
    'BKK',
    'APIVersion',
	FALSE,
    'ServerVersion',
    'LocationName',
    'TimeZone',
    '2023-12-27 12:34:56', -- Replace with actual server_time value
    '2023-12-27 12:34:56', -- Replace with actual game_time value
    0, -- Replace with actual player_count value
    100, -- 
    0, -- Replace with actual total_player_count value
    '0ms', -- Replace with actual network_ping value
    '0' -- Replace with actual network_packet value
);
