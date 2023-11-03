/*
Modify modelURL and serialPort to your settings
*/

const serialPort = 'COM7';
const setConfidence = 95; // from 0 - 100
		   	
// Voice [A=0, B=1 , Noise]
const modelURL = 'https://teachablemachine.withgoogle.com/models/ccq_o_1rP/';


let classifier,
	serial,
	label,
	conf = 0;

function preload() {
    classifier = ml5.soundClassifier(modelURL + 'model.json');
    serial = new p5.SerialPort();
}

function setup() {
    serial.open(serialPort);
    createCanvas(320, 240);
    classifier.classify(gotResult);
}

function draw() {
    background(0);
    fill(255);
    textSize(32);
    textAlign(CENTER);
    if (conf > setConfidence){
		text(label, width / 2, height - 4);
	}
}

function gotResult(error, results) {
    if (error) {
        console.error(error);
        return;
    }
    label = String(results[0].label);
    conf = Math.round(Number(results[0].confidence) * 10000) / 100;
    if (conf > setConfidence){
		console.log(label+' '+conf);
		serial.write(parseInt(label));
	}
}