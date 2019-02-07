// gui für robotersteuerung
function setup() {

	var h = windowHeight * 2 / 3;
	//var w = windowWidth * 2/3;
	var w = h * 2.2;
	var mycanvas = createCanvas(w, h);
	mycanvas.parent("robot_top");
	// zuordnung zu gui1
	frameRate(60);
	// alle 1/60 s
}

// winkel in bogenmaß
var pi = 3.14159265359;
var b0 = -pi / 10;
//first angle
var a1 = -3 / 4 * pi;
var a2 = 1.5 * pi;
var test = 0;
var s2active = false;
var s3active = false;
var b0_1000_last_frame = 0;

function draw() {
	background("#eff5f6");

	var s0x = windowWidth * 1 / 3;
	var s0y = windowHeight * 2 / 5;
	var l1 = windowHeight * 1 / 4.5 * 165 / 165;
	var l2 = windowHeight * 1 / 4.5 * 220 / 165;
	var l3 = windowHeight * 1 / 4.5 * 30 / 165;

	// line width
	var lineWidth = windowHeight * 1 / 40;

	//Koordinatensystem mit Ursprung (s1x, s1y), Winkel zu sO': b0
	var s1x = s0x;
	var s1y = s0y;
	//Koordinatensystem mit Ursprung (s2x, s2y), Winkel zu s1: a1
	var s2x = s0x + l1 * cos(b0);
	var s2y = s0y + l1 * sin(b0);
	//Koordinatensystem mit Urprung (s3x, s3y), Winkel zu s2: a2
	var s3x = s0x + l1 * cos(b0 + PI);
	var s3y = s0y + l1 * sin(b0 + PI);

	var b0_1000 = Math.round(b0 * 1000);

	//// Data sending to maintenance server
	function robot_data_send() {
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
			}
		};

		if (b0_1000 != b0_1000_last_frame) {
			xmlhttp.open("GET", "bosch2.html/query?b0_1000=" + b0_1000, true);
			xmlhttp.send();
		};

		// Data sending to robot server
	};

	function robot_data_send_robot_server() {
		var xmlhttp2 = new XMLHttpRequest();
		xmlhttp2.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
			}
		};

		if (b0_1000 != b0_1000_last_frame) {

			xmlhttp2.open("GET", "http://192.168.153.130:40000/bosch2.html/query?b0_1000=" + b0_1000, true);
			//xmlhttp2.setRequestHeader( 'Access-Control-Allow-Origin', '*');
			xmlhttp2.send();
		};

	};

	if (s2active || s3active) {
		robot_data_send();
		robot_data_send_robot_server();
	}

	if (mouseIsPressed) {
		if (mouseX > s2x - l3 / 3 && mouseX < s2x + l3 / 3 && mouseY > s2y - l3 / 3 && mouseY < s2y + l3 / 3 && mouseIsPressed && !s3active) {
			s2active = true;
			s3active = false;
		}

		if (mouseX > s3x - l3 / 3 && mouseX < s3x + l3 / 3 && mouseY > s3y - l3 / 3 && mouseY < s3y + l3 / 3 && mouseIsPressed && !s2active) {
			s2active = false;
			s3active = true;
		}

	} else {
		s2active = false;
		s3active = false;
	}

	b0_1000_last_frame = b0_1000;

	//recalculating angles of moving element
	if (s2active == true) {
		b0 = atan2(mouseY - s1y, mouseX - s1x);
	}
	if (s3active == true) {
		b0 = atan2(mouseY - s1y, mouseX - s1x) + PI;
	}

	// base top view
	strokeWeight(lineWidth * 0.5);
	stroke(0);
	ellipse(s1x, s1y, lineWidth * 4, lineWidth * 4);

	// roboter top view
	stroke(150);
	strokeWeight(lineWidth);
	if (s2active == true) {
		stroke(0);
	}
	line(s1x, s1y, s2x, s2y);
	if (s3active == true) {
		stroke(0);
	}
	line(s1x, s1y, s3x, s3y);

	//Joints
	strokeWeight(lineWidth / 5);
	stroke(0);
	ellipse(s1x, s1y, lineWidth * 0.8, lineWidth * 0.8);
	ellipse(s2x, s2y, lineWidth * 0.8, lineWidth * 0.8);
	ellipse(s3x, s3y, lineWidth * 0.8, lineWidth * 0.8);
	// Output of data

}

