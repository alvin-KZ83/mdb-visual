const LAYER_COUNT = 10; // Variable to keep track of the number of ring layers
let negative = true; // Added to play with monochromatic colors
let inverse = false; // Added to play with lerped color direction

let PARAMS = [
  // NOISE, PACE, FRQ
  [0.1, 0.1, 0.5]
]

let baseRadius;
let FREQ = 0.5;
let pulseAmplitude = 0.5;

let lastClickTime = 0;  // Store the time of the last click
let doubleClickThreshold = 300;  // Maximum time between clicks for a double-click (in milliseconds)
let clickTimeout;

let startX, endX;
let swiping = false;
let swipeThreshold = 100;

/*
  Additional section for connecting to heart rate monitor 
*/

let heartRate = 0;
let bleDevice;
let heartRateCharacteristic;

/*
  Additional section for connecting to video
*/

let video;

function setup() {
  createCanvas(windowWidth, windowHeight);

  // Request access to webcam
  let constraints = {
    video: true,
    audio: false
  };

  navigator.mediaDevices.getUserMedia(constraints)
    .then(function(stream) {
      video = createCapture(stream);
      video.size(width, height);
      video.hide(); // Hide default HTML video element
    })
    .catch(function(error) {
      console.error('Error accessing the camera:', error);
    });
}

function draw() {
  let BACKGROUND_COLOR = negative ? color('#e5d3b3') : color(30);
  let LAYER_COLOR = negative ? color('#664229') : color(255);

  background(BACKGROUND_COLOR);
  strokeWeight(5);
  noFill();

  translate(windowWidth / 2, windowHeight / 2);

  // const NOISE = PARAMS[0][0];   // 0.10 to 1.00
  // const PACE  = PARAMS[0][1];   // 0.01 to 0.10
  // const FREQ  = PARAMS[0][2];   // 0.00 to 0.00

  let NOISE = (heartRate) < 100 ? 0 : map(heartRate, 100, 160, 0.1, 1)
  let PACE = (heartRate) < 100 ? 0 : map(heartRate, 100, 160, 0.01, 0.1)
  let FREQ = (heartRate) < 80 ? 0.1 : map(heartRate, 80, 160, 0, 1)

  // every 10 above a hundred introduces the noise
  // under 100, it should remain normal pulsing and stay circle

  baseRadius = windowHeight * 0.1 + sin(frameCount * FREQ) * pulseAmplitude * windowHeight * 0.1;

  for (let layer = 0; layer < LAYER_COUNT; layer++) {
    let radius = baseRadius + layer * 20;
    let noiseOffsetScale = layer * NOISE;
    let colorFactor = map(layer, 0, LAYER_COUNT, 0, 1);
    let lerpedColor = inverse ? lerpColor(BACKGROUND_COLOR, LAYER_COLOR, colorFactor) : lerpColor(LAYER_COLOR, BACKGROUND_COLOR, colorFactor);

    stroke(lerpedColor);

    beginShape();
    for (let i = 0; i < 360; i++) {
      let angle = i * TWO_PI / 360;

      let layerNoiseOffeset = layer * 0.1;
      let timeOffset = frameCount * PACE + layerNoiseOffeset;

      let noiseOffset = noise(
        cos(angle) * noiseOffsetScale + timeOffset,
        sin(angle) * noiseOffsetScale + timeOffset,
        timeOffset
      );

      let r = radius + (NOISE * noiseOffset * 50);

      let x = r * cos(angle);
      let y = r * sin(angle);

      vertex(x, y);
    }
    endShape(CLOSE);
  }

  // HR
  noStroke(LAYER_COLOR);
  fill(LAYER_COLOR);
  textSize(20);
  textAlign(CENTER, CENTER);
  text(`${heartRate}`, 0, 0);

  if (video) {
    image(video, -windowWidth / 2 + 50, -windowHeight / 2 + 50, 3 * 180, 3 * 90); // Tailored to S25
  }
}


async function connectToBLE() {
  try {
    // Request the BLE device
    bleDevice = await navigator.bluetooth.requestDevice({
      filters: [{ services: ['heart_rate'] }]
    });

    // Connect to the GATT server
    const server = await bleDevice.gatt.connect();

    // Get the Heart Rate service
    const service = await server.getPrimaryService('heart_rate');

    // Get the Heart Rate Measurement characteristic
    heartRateCharacteristic = await service.getCharacteristic('heart_rate_measurement');

    // Enable notifications
    heartRateCharacteristic.startNotifications();
    heartRateCharacteristic.addEventListener('characteristicvaluechanged', handleHeartRate);

    console.log("Connected to BLE Heart Rate Sensor");

  } catch (error) {
    console.error("BLE Connection Error: ", error);
  }
}

function handleHeartRate(event) {
  let value = event.target.value;
  let heartRateValue = value.getUint8(1); // Extract heart rate from the data
  heartRate = heartRateValue;
}

function doubleClicked() {
  negative = !negative
}

function mousePressed() {
  // Start of the swipe (when mouse is pressed)
  startX = mouseX;
  swiping = true;
}

function mouseReleased() {
  // End of the swipe (when mouse is released)
  endX = mouseX;

  // Check if the swipe is horizontal and has moved far enough
  if (swiping && abs(endX - startX) > swipeThreshold) {
    if (endX > startX) {
      console.log("Swipe Right");
      // Add your right swipe logic here
    } else {
      console.log("Swipe Left");
      // Add your left swipe logic here
    }
  }

  // Reset swipe state
  swiping = false;
}

document.querySelector('#connectBluetooth').addEventListener('click', e => connectToBLE());

/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */
'use strict';

// Put variables in global scope to make them available to the browser console.
const constraints = window.constraints = {
  audio: false,
  video: true
};

function handleSuccess(stream) {
  const video = document.querySelector('video');
  const videoTracks = stream.getVideoTracks();
  console.log('Got stream with constraints:', constraints);
  console.log(`Using video device: ${videoTracks[0].label}`);
  window.stream = stream; // make variable available to browser console
  video.srcObject = stream;
}

function handleError(error) {
  if (error.name === 'OverconstrainedError') {
    errorMsg(`OverconstrainedError: The constraints could not be satisfied by the available devices. Constraints: ${JSON.stringify(constraints)}`);
  } else if (error.name === 'NotAllowedError') {
    errorMsg('NotAllowedError: Permissions have not been granted to use your camera and ' +
      'microphone, you need to allow the page access to your devices in ' +
      'order for the demo to work.');
  }
  errorMsg(`getUserMedia error: ${error.name}`, error);
}

function errorMsg(msg, error) {
  const errorElement = document.querySelector('#errorMsg');
  errorElement.innerHTML += `<p>${msg}</p>`;
  if (typeof error !== 'undefined') {
    console.error(error);
  }
}

async function init(e) {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
    e.target.disabled = true;
  } catch (e) {
    handleError(e);
  }
}

document.querySelector('#showVideo').addEventListener('click', e => init(e));