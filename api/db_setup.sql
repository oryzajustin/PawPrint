CREATE TABLE camera
(
	id INT NOT NULL AUTO_INCREMENT,
	latitude FLOAT(10,7) NOT NULL,
	longitude FLOAT(10,7) NOT NULL,
	url varchar(255) NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE request
(
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(255) NULL,
	phone VARCHAR(255) NOT NULL,
	animal_type VARCHAR(255) NOT NULL,
	bound_north FLOAT(10,7) NOT NULL,
	bound_south FLOAT(10,7) NOT NULL,
	bound_east FLOAT(10,7) NOT NULL,
	bound_west FLOAT(10,7) NOT NULL,
	found BIT(1) NOT NULL DEFAULT FALSE,
	PRIMARY KEY PK_REQUEST (id)
);

CREATE TABLE requestCamera
(
	request_id INT NOT NULL,
	camera_id INT NOT NULL,
	PRIMARY KEY PK_REQUESTCAMERA (request_id, camera_id),
	CONSTRAINT FK_REQUESTCAMERA_REQUEST FOREIGN KEY (request_id) REFERENCES request(id) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT FK_REQUESTCAMERA_CAMERA FOREIGN KEY (camera_id) REFERENCES camera(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE foundanimal
(
	id INT NOT NULL AUTO_INCREMENT,
	camera_id INT NOT NULL,
	type VARCHAR(255) NOT NULL,
	img VARCHAR(255) NOT NULL,
	PRIMARY KEY PK_FOUND (id),
	CONSTRAINT FK_FOUNDANIMAL_CAMERA FOREIGN KEY (camera_id) REFERENCES camera(id) ON UPDATE CASCADE ON DELETE CASCADE
);


#ALTER TABLE foundanimal ADD COLUMN camera_id INT NOT NULL, ADD CONSTRAINT FK_FOUNDANIMAL_CAMERA FOREIGN KEY (camera_id) REFERENCES camera(id) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE TABLE requestFound
(
	request_id INT NOT NULL,
	foundanimal_id INT NOT NULL,
	slug VARCHAR(255) NOT NULL,
	PRIMARY KEY PK_REQUESTFOUND (request_id, foundanimal_id),
	CONSTRAINT FK_REQUESTFOUND_REQUEST FOREIGN KEY (request_id) REFERENCES request(id) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT FK_REQUESTFOUND_FOUNDANIMAL FOREIGN KEY (foundanimal_id) REFERENCES foundanimal(id) ON UPDATE CASCADE ON DELETE CASCADE
);


/*
INITIAL DATA

INSERT INTO camera
(latitude, longitude, url)
VALUES
(42.35543, -71.06277, 'http://24.147.70.250:8081/mjpg/video.mjpg?COUNTER'),
(42.356429999999996, -71.06262714285714, 'http://96.92.105.137:80/cgi-bin/viewer/video.jpg?r=COUNTER'),
(42.35743, -71.06248428571429, 'http://173.9.39.69:80/cgi-bin/viewer/video.jpg?r=COUNTER'),
(42.35843, -71.06234142857143, 'http://98.110.196.91:81/__live.jpg?&&&'),
(42.359429999999996, -71.06219857142857, 'http://70.188.190.79:88/videostream.cgi?user=admin&pwd='),
(42.36043, -71.06205571428572, 'http://216.236.251.135:80/mjpg/video.mjpg?COUNTER'),
(42.36143, -71.06191285714286, 'http://24.63.140.124:80/mjpg/video.mjpg?COUNTER'),
(42.35543, -71.06177, 'http://75.67.41.92:4000/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.356429999999996, -71.06162714285715, 'http://96.93.156.202:50000/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.35743, -71.06148428571429, 'http://71.248.172.3:50001/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.35843, -71.06134142857142, 'http://73.219.239.63:84/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.359429999999996, -71.06119857142858, 'http://73.219.239.63:86/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.36043, -71.06105571428571, 'http://155.41.145.67:80/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.36143, -71.06091285714285, 'http://96.237.61.111:81/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.35543, -71.06077, 'http://96.237.61.111:82/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.356429999999996, -71.06062714285714, 'http://96.237.61.111:83/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.35743, -71.06048428571428, 'http://73.218.239.179:90/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.35843, -71.06034142857143, 'http://168.122.98.50:80/cgi-bin/camera?resolution=640&amp;quality=1&amp;Language=0&amp;COUNTER'),
(42.359429999999996, -71.06019857142857, 'http://72.93.94.34:80/oneshotimage1?COUNTER'),
(42.36043, -71.06005571428571, 'http://50.204.85.33:80/mjpg/video.mjpg?COUNTER'),
(42.36143, -71.05991285714286, 'http://24.147.16.252:8081/mjpg/video.mjpg?COUNTER'),
(42.35543, -71.05977, 'http://24.147.16.252:8082/mjpg/video.mjpg?COUNTER'),
(42.356429999999996, -71.05962714285714, 'http://24.147.16.252:8083/mjpg/video.mjpg?COUNTER'),
(42.35743, -71.05948428571429, 'http://24.147.16.252:8080/mjpg/video.mjpg?COUNTER'),
(42.35843, -71.05934142857143, 'http://173.14.183.117:80/oneshotimage1?COUNTER'),
(42.359429999999996, -71.05919857142857, 'http://50.195.50.214:8082/mjpg/video.mjpg?COUNTER'),
(42.36043, -71.05905571428572, 'http://50.79.170.234:80/mjpg/video.mjpg?COUNTER'),
(42.344869, -71.09599385714286, 'http://129.10.161.241:80/mjpg/video.mjpg?COUNTER'),
(42.35543, -71.05877, 'http://108.49.186.55:80/mjpg/video.mjpg?COUNTER'),
(42.356429999999996, -71.05862714285715, 'http://108.49.186.56:80/mjpg/video.mjpg?COUNTER'),
(42.35743, -71.05848428571429, 'http://71.251.21.66:80/mjpg/video.mjpg?COUNTER'),
(42.35843, -71.05834142857142, 'http://108.49.138.78:80/mjpg/video.mjpg?COUNTER'),
(42.359429999999996, -71.05819857142858, 'http://199.94.69.102:80/mjpg/video.mjpg?COUNTER'),
(42.36043, -71.05805571428571, 'http://50.241.95.106:80/mjpg/video.mjpg?COUNTER'),
(42.36143, -71.05791285714285, 'http://173.166.10.122:80/mjpg/video.mjpg?COUNTER'),
(42.35543, -71.05777, 'http://50.78.17.145:8001/mjpg/video.mjpg?COUNTER'),
(42.339869, -71.09470814285714, 'http://129.10.130.155:80/mjpg/video.mjpg?COUNTER'),
(42.35743, -71.05748428571428, 'http://173.14.183.116:80/oneshotimage1?COUNTER'),
(42.35843, -71.05734142857143, 'http://173.9.43.97:86/mjpg/video.mjpg?COUNTER'),
(42.359429999999996, -71.05719857142857, 'http://173.9.43.97:84/mjpg/video.mjpg?COUNTER'),
(42.36043, -71.05705571428571, 'http://23.235.111.74:8090/videostream.cgi?user=admin&pwd='),
(42.36143, -71.05691285714286, 'http://128.197.128.160:80/mjpg/video.mjpg?COUNTER');
*/