var APP_ID = 'amzn1.ask.skill.1774a50a-ce30-4dd3-bf22-d4858dac2e3f'; // This is the amazon skill ID
var AlexaSkill = require('./AlexaSkill');
var ROSLIB = require('roslib')


var ros = new ROSLIB.Ros({
    url : 'INSERT YOURS HERE'
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
        var msg = new ROSLIB.Message({
            data : intent.slots.Message.value
        });
        speech.publish(msg);
	response.ask('');
    },
    "AMAZON.StopIntent": function (intent, session, response) {
        response.tell('goodbye');
    },
    "AMAZON.CancelIntent": function (intent, session, response) {
        response.tell('');
    }
};

// Create the handler that responds to the Alexa Request.
exports.handler = function (event, context) {
    // Create an instance of the TM skill.
    var tm = new TM();
    tm.execute(event, context);
};
