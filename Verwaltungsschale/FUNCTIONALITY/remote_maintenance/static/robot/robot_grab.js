// gui für robotersteuerung
// Author: Vladimir Kutscher
// Author: Syed Emad
function setup() {

	var h = windowHeight * 2 / 3;
	if(windowHeight>windowWidth){
		var w = windowWidth * 2/3;
	}else{
		var w = windowWidth * 2/3;
	}


	var mycanvas = createCanvas(w, h);
	mycanvas.parent("robot_grab");
	// zuordnung zu gui1
	frameRate(60);
	// alle 1/60 s
}

// winkel in bogenmaß
var PI = 3.14159265359;
var pi = 3.14159265359;
var c0 = -pi / 2;
var c0_out=0;
//first angle

var position_http = new XMLHttpRequest();
position_http.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
	}
	//document.getElementById("demo").innerHTML = this.responseText;;
	var obj = this.responseText;
	var obj1 = JSON.parse(obj);
	c0 = obj1.c0-pi	;
};
position_http.open("GET", "current_position", true);
position_http.send();


var circle_point_active = false;
var slider_active = false;
var slider_ratio = 0;
var x_sliderArm;
var y_sliderArm;
var c0_1000_last_frame = 0;

function draw() {
	background("#eff5f6");

	// line width
	var lineWidth = windowHeight * 1 / 40;
	var l1 = lineWidth * 2;
	//windowHeight * 1 / 4.5 * 165 / 165;
	var l2 = windowHeight * 1 / 4.5 * 220 / 165;
	var l3 = windowHeight * 1 / 4.5 * 30 / 165;

	var x_sliderArm_start = windowWidth * 3.2 / 5;
	var y_sliderArm_start = windowHeight * 2.8 / 5;
	var x_sliderArm_start2 = x_sliderArm_start - l1 * 3;
	var y_sliderArm_start2 = y_sliderArm_start;
	var l_grab = x_sliderArm_start2 - x_sliderArm_start;

	// mid for 3d grafic grab rotation
	var x_mid_grab = windowWidth * 1 / 3;
	var y_mid_grab = windowHeight * 1 / 3;

	// midpoint circle for rotation
	var x_circle_mid = windowWidth* 1 / 15;
	var y_circle_mid = windowHeight * 2.5 / 5;
	;
	// roation point for grab roation "joystick"
	var x_circle_point = x_circle_mid + l1 * cos(c0);
	var x_circle_point_correct = x_circle_mRobot topid + l1 * cos(c0+PI/4*3);
	var y_circle_point = y_circle_mid + l1 * sin(c0);
	var y_circle_point_correct = y_circle_mid + l1 * sin(c0+PI/4*3);
	var x_slider_point = x_sliderArm_start + slider_ratio * l_grab;

	var c0_1000 = Math.round(c0 * 1000);
	c0_out=c0+PI;
	var c0_out_1000=Math.round(c0_1000+PI*1000);
	var slider_ratio_1000=Math.round(slider_ratio*PI*1000);
	function robot_data_send() {
		var xmlhttp = new XMLHttpRequest();
		xmlhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
			}
		};

		if (c0_1000 != c0_1000_last_frame || slider_ratio != slider_ratio_last_frame) {
			xmlhttp.open("GET", "control?view=3&c0_1000=" + c0_out_1000 + "&slider_ratio=" + slider_ratio_1000, true);
			xmlhttp.send();
		};

	};



	if (circle_point_active || slider_active) {
		robot_data_send();
	}

	// is the circle element active?
	if (mouseIsPressed) {
		if (mouseX > x_circle_point - lineWidth * 4 && mouseX < x_circle_point + lineWidth * 4 && mouseY > y_circle_point - lineWidth * 4 && mouseY < y_circle_point + lineWidth * 4 && mouseIsPressed) {
			circle_point_active = true;
		}
	} else {
		circle_point_active = false;
	}

	// This is the data which was send - save for comparison in next frame
	slider_ratio_last_frame = slider_ratio;
	c0_1000_last_frame = c0_1000;

	//recalculating angles of moving circle element for rotation
	if (circle_point_active == true) {

		c0 = atan2(mouseY - y_circle_mid, mouseX - x_circle_mid);
		if (c0>=PI/2){
			c0=-PI;
		}
		if (c0>= 0){
			if (c0<PI/2)
			c0=0;
		}
	}

	// is the slider active?
	if (mouseIsPressed) {
		if (mouseX > x_slider_point - lineWidth * 4 && mouseX < x_slider_point + lineWidth * 4 && mouseY > y_sliderArm_start - lineWidth * 4 && mouseY < y_sliderArm_start + lineWidth * 4 && mouseIsPressed) {
			slider_active = true;
		}
	} else {
		slider_active = false;
	}

	//recalculating position of slider
	if (slider_active == true) {

		x_sliderArm = Math.min(Math.max(mouseX, x_sliderArm_start2), x_sliderArm_start);
		slider_ratio = (x_sliderArm_start - x_sliderArm) / (abs(x_sliderArm_start2 - x_sliderArm_start));
	}

	// circle for rotation
	strokeWeight(lineWidth * 0.25);
	stroke(125);
	var r_x=lineWidth * 4;
	var r_y=lineWidth * 4;
	ellipse(x_circle_mid, y_circle_mid, r_x, r_y);

	//Rotation point
	strokeWeight(lineWidth * 1.2);
	stroke(0);
	line(x_circle_point, y_circle_point, x_circle_point, y_circle_point);

	// open/close control slider
	strokeWeight(lineWidth);
	stroke(125);
	line(x_sliderArm_start, y_sliderArm_start, x_sliderArm_start2, y_sliderArm_start2);

	//open/close slider point x_axis
	strokeWeight(lineWidth * 1.2);
	stroke(0);
	line(x_sliderArm_start + slider_ratio * l_grab, y_sliderArm_start + slider_ratio, x_sliderArm_start + slider_ratio * l_grab, y_sliderArm_start + slider_ratio);

	//grab 3d grafic circle
	strokeWeight(lineWidth * 0.2);
	stroke(0);
	ellipse(x_mid_grab, y_mid_grab, lineWidth * 20, lineWidth * 20);

	////////////////////GRAB 3D GRADIC GRAB
	var c0_correct=c0-PI/4*3;
	////////coordinates 3d grafic grab
	var x_grab_end1 = x_mid_grab + l_grab / 1.5 * Math.cos(PI / 4) * Math.cos(c0_correct - PI / 4);
	var y_grab_end1 = y_mid_grab + l_grab / 1.5 * Math.sin(PI / 4) * Math.sin(c0_correct - PI / 4);
	var x_grab_end2 = x_mid_grab - l_grab / 1.5 * Math.cos(PI / 4) * Math.cos(c0_correct - PI / 4);
	var y_grab_end2 = y_mid_grab - l_grab / 1.5 * Math.sin(PI / 4) * Math.sin(c0_correct - PI / 4);

	// postion of grab arms
	var x_grab_pos1 = x_grab_end1 - l_grab / 2 * Math.cos(PI / 4) * (slider_ratio * 1.1) * Math.cos(c0_correct - PI / 4);
	var y_grab_pos1 = y_grab_end1 - l_grab / 2 * Math.sin(PI / 4) * (slider_ratio * 1.1) * Math.sin(c0_correct - PI / 4);
	var x_grab_pos2 = x_grab_end2 + l_grab / 2 * Math.cos(PI / 4) * (slider_ratio * 1.1) * Math.cos(c0_correct - PI / 4);
	var y_grab_pos2 = y_grab_end2 + l_grab / 2 * Math.sin(PI / 4) * (slider_ratio * 1.1) * Math.sin(c0_correct - PI / 4);

	// 3d grab line structure/animation
	strokeWeight(lineWidth);
	//arm before grab
	stroke(200);
	line(x_mid_grab, y_mid_grab, x_mid_grab + Math.cos(PI / 4) * l_grab, y_mid_grab - Math.sin(PI / 4) * l_grab);


	if (Math.cos(c0) < 0) {
		//grab arms
		strokeWeight(lineWidth);
		stroke(150 - Math.sin(c0 - PI / 2) * 20);
		line(x_mid_grab, y_mid_grab, x_grab_end2, y_grab_end2);
		stroke(150 + Math.sin(c0 - PI / 2) * 20);
		line(x_grab_end1, y_grab_end1, x_mid_grab, y_mid_grab);
		stroke(0);
		strokeWeight(lineWidth / 8);
		ellipse(x_mid_grab, y_mid_grab, lineWidth * 0.8, lineWidth);
		strokeWeight(lineWidth);
		stroke(150 - Math.sin(c0 - PI / 2) * 20);
		line(x_grab_pos2, y_grab_pos2, x_grab_pos2 - Math.cos(PI / 4) * l_grab * 2 / 3, y_grab_pos2 + Math.cos(PI / 4) * l_grab * 2 / 3);
		stroke(150 + Math.sin(c0 - PI / 2) * 20);
		line(x_grab_pos1, y_grab_pos1, x_grab_pos1 - Math.cos(PI / 4) * l_grab * 2 / 3, y_grab_pos1 + Math.cos(PI / 4) * l_grab * 2 / 3);


	} else {


				//grab arms
		stroke(150 + Math.sin(c0 - PI / 2) * 20);
		line(x_grab_end1, y_grab_end1, x_mid_grab, y_mid_grab);
		stroke(150 - Math.sin(c0 - PI / 2) * 20);
		line(x_mid_grab, y_mid_grab, x_grab_end2, y_grab_end2);
		stroke(0);
		strokeWeight(lineWidth / 8);
		ellipse(x_mid_grab, y_mid_grab, lineWidth * 0.8, lineWidth);
		strokeWeight(lineWidth);
		stroke(150 + Math.sin(c0 - PI / 2) * 20);
		line(x_grab_pos1, y_grab_pos1, x_grab_pos1 - Math.cos(PI / 4) * l_grab * 2 / 3, y_grab_pos1 + Math.cos(PI / 4) * l_grab * 2 / 3);
		stroke(150 - Math.sin(c0 - PI / 2) * 20);
		line(x_grab_pos2, y_grab_pos2, x_grab_pos2 - Math.cos(PI / 4) * l_grab * 2 / 3, y_grab_pos2 + Math.cos(PI / 4) * l_grab * 2 / 3);
	};
	$("#c0_out").text(c0_out / PI * 180);
	$("#c0").text(c0 / PI * 180);
	$("#c0_diff").text(c0_out-c0 / PI * 180);
};
