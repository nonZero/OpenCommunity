"use strict";

$(function() {

	var pieData = [{
		value : 30,
		color : "red"
	}, {
		value : 50,
		color : "green"
	}, {
		value : 200,
		color : "yellow"
	}];

	var actions = {
		//Boolean - Whether we should show a stroke on each segment
		segmentShowStroke : true,

		//String - The colour of each segment stroke
		segmentStrokeColor : "#fff",

		//Number - The width of each segment stroke
		segmentStrokeWidth : 2,

		//Boolean - Whether we should animate the chart
		animation : false,

		//Number - Amount of animation steps
		animationSteps : 100,

		//String - Animation easing effect
		animationEasing : "easeOutBounce",

		//Boolean - Whether we animate the rotation of the Pie
		animateRotate : false,

		//Boolean - Whether we animate scaling the Pie from the centre
		animateScale : false,

		//Function - Will fire on animation completion.
		onAnimationComplete : null
	};

	// var myPie = new Chart($("#proposalChart").get(0).getContext("2d")).Pie(pieData, actions);

});