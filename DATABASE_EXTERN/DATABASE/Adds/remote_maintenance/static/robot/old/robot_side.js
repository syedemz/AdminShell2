// gui für robotersteuerung

function setup() {

	var h = windowHeight * 2 / 3;
	//var w = windowWidth * 2/3;
	var w = h * 2.2;
	var mycanvas = createCanvas(w, h);
	mycanvas.parent("robot_side");
	// zuordnung zu gui1
	frameRate(1000);
	// alle 1/60 s
};

// winkel in bogenmaß
var pi = 3.14159265359;
var a0 = -pi / 10;
//first angle
var a1 = -3 / 4 * pi;
var a2 = 1.5 * pi;
var test = 0;
var s2active = false;
var s3active = false;
var s4active = false;
// This is the data which was send
var a0_1000_last_frame = 0;
var a1_1000_last_frame = 0;
var a2_1000_last_frame = 0;
var s4y_last_frame = 0;

function draw() {
	background("#eff5f6");

	var s0x = windowWidth * 1 / 3;
	var s0y = windowHeight * 3 / 5;
	var l1 = windowHeight * 1 / 4.5 * 165 / 165;
	var l2 = windowHeight * 1 / 4.5 * 220 / 165;
	var l3 = windowHeight * 1 / 4.5 * 30 / 165;

	// line width
	var lineWidth = (windowHeight * 1 / 40);

	//Koordinatensystem mit Ursprung (s1x, s1y), Winkel zu sO': a0
	var s1x = s0x;
	var s1y = s0y;
	//Koordinatensystem mit Ursprung (s2x, s2y), Winkel zu s1: a1
	var s2x = s0x + l1 * cos(a0);
	var s2y = s0y + l1 * sin(a0);
	//Koordinatensystem mit Urprung (s3x, s3y), Winkel zu s2: a2
	var s3x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0);
	var s3y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0);
	//Berechnung des Toolcenterpoints s4
	var s4x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0) + l3 * cos(a2 + a1 + a0);
	var s4y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0) + l3 * sin(a2 + a1 + a0);

	var a0_1000 = Math.round(a0 * 1000);
	var a1_1000 = Math.round(a1 * 1000);
	var a2_1000 = Math.round(a2 * 1000);

	function robot_data_send() {
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
			}
		};

		if (a0_1000 != a0_1000_last_frame || a1_1000 != a1_1000_last_frame || a2_1000 != a2_1000_last_frame) {

			//xmlhttp.open("GET", "http://130.83.87.222:60000/bosch2.html/query?a0_1000=" + a0_1000 + "&a1_1000=" + a1_1000 + "&a2_1000=" + a2_1000, true);
			//xmlhttp.open("GET", "http://127.0.0.1:50000/bosch2.html/query?a0_1000=" + a0_1000 + "&a1_1000=" + a1_1000 + "&a2_1000=" + a2_1000, true);
			xmlhttp.open("GET", "bosch2.html/query?a0_1000=" + a0_1000 + "&a1_1000=" + a1_1000 + "&a2_1000=" + a2_1000, true);
			xmlhttp.send();
		};

	};

	function robot_data_send_robot_server() {
		var xmlhttp2 = new XMLHttpRequest();
		xmlhttp2.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
			}
		};

		if (a0_1000 != a0_1000_last_frame || a1_1000 != a1_1000_last_frame || a2_1000 != a2_1000_last_frame) {

			//xmlhttp2.open("GET", "http://130.83.87.222:60000/bosch2.html/query?a0_1000=" + a0_1000 + "&a1_1000=" + a1_1000 + "&a2_1000=" + a2_1000, true);
			xmlhttp2.open("GET", "http://127.0.0.1:40000/bosch2.html/query?a0_1000=" + a0_1000 + "&a1_1000=" + a1_1000 + "&a2_1000=" + a2_1000, true);
			//xmlhttp2.setRequestHeader( 'Access-Control-Allow-Origin', '*');
			xmlhttp2.send();
		};

	};


	if (s2active || s3active || s4active) {
		robot_data_send();
		//robot_data_send_robot_server();
	}

	if (mouseIsPressed) {
		if (mouseX > s2x - l3 / 3 && mouseX < s2x + l3 / 3 && mouseY > s2y - l3 / 3 && mouseY < s2y + l3 / 3 && mouseIsPressed && !s3active && !s4active) {
			s2active = true;
			s3active = false;
			s4active = false;
		}

		if (mouseX > s3x - l3 / 3 && mouseX < s3x + l3 / 3 && mouseY > s3y - l3 / 3 && mouseY < s3y + l3 / 3 && mouseIsPressed && !s2active && !s4active) {
			s2active = false;
			s3active = true;
			s4active = false;
		}

		if (mouseX > s4x - l3 / 3 && mouseX < s4x + l3 / 3 && mouseY > s4y - l3 / 3 && mouseY < s4y + l3 / 3 && mouseIsPressed && !s2active && !s3active) {
			s2active = false;
			s3active = false;
			s4active = true;
		}
	} else {
		s2active = false;
		s3active = false;
		s4active = false;
	}

	// This is the data which was send
	a0_1000_last_frame = a0_1000;
	a1_1000_last_frame = a1_1000;
	a2_1000_last_frame = a2_1000;

	//recalculating angles of moving elements
	if (s4y < s0y && s3y < s0y && s2y < s0y) {

		if (s2active == true) {
			//a0 = atan2(mouseY - s1y, mouseX - s1x);
			//a0 = constrain(a0, -PI, 0);
			if (a0 > 0) {
				a0 = 0;
			} else if (a0 < -PI) {
				a0 = -PI;
			} else {
				a0 = atan2(mouseY - s1y, mouseX - s1x);
			}

		}
		if (s3active == true) {
			a1 = atan2(mouseY - s2y, mouseX - s2x) - a0;
			//if (a1<=-PI){a1=-PI}
			if (a1 >= 0) {
				if (a1 <= PI) {
					if (a1 > PI / 2) {
						a1 = PI;
					} else {
						a1 = 0;
					}
				}
			}
		}
		if (s4active == true) {
			a2 = atan2(mouseY - s3y, mouseX - s3x) - a1 - a0;
			// a2 = constrain(a2, -PI, PI)
		}
	} else {
		if (a0 < -PI / 36) {
			while (s4y >= s0y || s3y >= s0y || s2y >= s0y) {
				if (s2y >= s0y) {
					a0 = a0 + PI / 500;
					//Koordinatensystem mit Ursprung (s2x, s2y), Winkel zu s1: a1
					var s2x = s0x + l1 * cos(a0);
					var s2y = s0y + l1 * sin(a0);
					//Koordinatensystem mit Urprung (s3x, s3y), Winkel zu s2: a2
					var s3x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0);
					var s3y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0);
					//Berechnung des Toolcenterpoints s4
					var s4x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0) + l3 * cos(a2 + a1 + a0);
					var s4y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0) + l3 * sin(a2 + a1 + a0);
				}
				if (s3y >= s0y) {
					a0 = a0 + PI / 500;
					//Koordinatensystem mit Urprung (s3x, s3y), Winkel zu s2: a2
					var s3x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0);
					var s3y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0);
					//Berechnung des Toolcenterpoints s4
					var s4x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0) + l3 * cos(a2 + a1 + a0);
					var s4y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0) + l3 * sin(a2 + a1 + a0);
				}
				if (s4y >= s0y) {
					a0 = a0 + PI / 500;
					//Berechnung des Toolcenterpoints s4
					var s4x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0) + l3 * cos(a2 + a1 + a0);
					var s4y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0) + l3 * sin(a2 + a1 + a0);
				}
			}

		} else {
			while (s4y >= s0y || s3y >= s0y || s2y >= s0y) {
				if (s2y >= s0y) {
					a0 = a0 - PI / 500;
					//Koordinatensystem mit Ursprung (s2x, s2y), Winkel zu s1: a1
					var s2x = s0x + l1 * cos(a0);
					var s2y = s0y + l1 * sin(a0);
					//Koordinatensystem mit Urprung (s3x, s3y), Winkel zu s2: a2
					var s3x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0);
					var s3y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0);
					//Berechnung des Toolcenterpoints s4
					var s4x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0) + l3 * cos(a2 + a1 + a0);
					var s4y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0) + l3 * sin(a2 + a1 + a0);
				}
				if (s3y >= s0y) {
					a1 = a1 + PI / 500;
					//Koordinatensystem mit Urprung (s3x, s3y), Winkel zu s2: a2
					var s3x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0);
					var s3y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0);
					//Berechnung des Toolcenterpoints s4
					var s4x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0) + l3 * cos(a2 + a1 + a0);
					var s4y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0) + l3 * sin(a2 + a1 + a0);
				}
				if (s4y >= s0y) {
					a1 = a1 + PI / 500;
					//Berechnung des Toolcenterpoints s4
					var s4x = s0x + l1 * cos(a0) + l2 * cos(a1 + a0) + l3 * cos(a2 + a1 + a0);
					var s4y = s0y + l1 * sin(a0) + l2 * sin(a1 + a0) + l3 * sin(a2 + a1 + a0);
				}
			}
		}

		s2active = false;
		s3active = false;
		s4active = false;
	}

	s4y_last_frame = s4y;

	// base side view
	strokeWeight(lineWidth);
	stroke(0);
	line(s1x, s1y, s1x, s1y + l3);
	stroke(0);
	line(s1x + 1.5 * l3, s1y + l3, s1x - 1.5 * l3, s1y + l3);

	// roboter side view
	stroke(150);
	strokeWeight(lineWidth);
	if (s2active == true) {
		stroke(0);
	}

	line(s1x, s1y, s2x, s2y);
	stroke(150);
	if (s3active == true) {
		stroke(0);
	}
	line(s2x, s2y, s3x, s3y);
	stroke(150);
	if (s4active == true) {
		stroke(0);
	}
	line(s3x, s3y, s4x, s4y);

	//Joints
	strokeWeight(lineWidth / 5);
	stroke(0);
	ellipse(s1x, s1y, lineWidth * 0.8, lineWidth * 0.8);
	ellipse(s2x, s2y, lineWidth * 0.8, lineWidth * 0.8);
	ellipse(s3x, s3y, lineWidth * 0.8, lineWidth * 0.8);
	ellipse(s4x, s4y, lineWidth * 0.8, lineWidth * 0.8);

	// Output of data

	$("#a0").text(a0 / PI * 180);
	$("#a1").text(a1 / PI * 180);
	$("#a2").text(a2 / PI * 180);
}

