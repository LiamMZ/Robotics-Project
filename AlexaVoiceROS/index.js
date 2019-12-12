var APP_ID = 'amzn1.ask.skill.1774a50a-ce30-4dd3-bf22-d4858dac2e3f'; // This is the amazon skill ID
var AlexaSkill = require('./AlexaSkill');
var ROSLIB = require('roslib')


var ros = new ROSLIB.Ros({
<<<<<<< HEAD
    url : 'wss://localhost:9090' // This was a test I did at home using my public ip(port 9090 is what ROS defaults to)
=======
    url : 'INSERT YOURS HERE'
>>>>>>> 22775a8f1df521e1f06506eea526047dc9e4de96
});

var talk = 'not connected';
ros.on('connection', function() {
    console.log('Connected to websocket server.');
    talk = 'connected to octopus';
});

ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
});

ros.on('close', function() {
    console.log('Connection to websocket server closed.');
});

var speech = new ROSLIB.Topic({
    ros : ros,
    name : '/speech_recognition',
    messageType : 'std_msgs/String'
});

var helpText = "I can send a message to sawyer";

var TM = function () {
    AlexaSkill.call(this, APP_ID);
};

// Extend AlexaSkill
TM.prototype = Object.create(AlexaSkill.prototype);
TM.prototype.constructor = TM;

TM.prototype.eventHandlers.onSessionStarted = function (sessionStartedRequest, session) {
    console.log("Session Started");
};

TM.prototype.eventHandlers.onLaunch = function (launchRequest, session, response) {
    var speechOutput = "Welcome to the Intro To Robotics Final Project!, " + helpText;
    var repromptText = helpText;

    //response.ask(speechOutput, repromptText);
};

TM.prototype.eventHandlers.onSessionEnded = function (sessionEndedRequest, session) {
    console.log("Session Closed");
};

TM.prototype.intentHandlers = {
    "MessageIntent": function (intent, session, response) {
<<<<<<< HEAD
        var msg = new ROSLIB.Message({ // "item" is the slot value turned to text
            data : intent.slots.item.value
        });
        speech.publish(msg);
	    response.ask('Testing.'); // This is for testing, remove later?
=======
        var msg = new ROSLIB.Message({
            data : intent.slots.Message.value
        });
        speech.publish(msg);
	response.ask('');
>>>>>>> 22775a8f1df521e1f06506eea526047dc9e4de96
    },
    "AMAZON.StopIntent": function (intent, session, response) {
        response.tell('goodbye');
    },
    "AMAZON.CancelIntent": function (intent, session, response) {
<<<<<<< HEAD
        response.tell('Cancelling');
=======
        response.tell('');
>>>>>>> 22775a8f1df521e1f06506eea526047dc9e4de96
    }
};

// Create the handler that responds to the Alexa Request.
exports.handler = function (event, context) {
    // Create an instance of the TM skill.
    var tm = new TM();
    tm.execute(event, context);
};
