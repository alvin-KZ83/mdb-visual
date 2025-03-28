const LAYER_COUNT = 10; // Variable to keep track of the number of ring layers
let negative = true; // Added to play with monochromatic colors
let inverse = false; // Added to play with lerped color direction

let PARAMS = [
  // NOISE, PACE, FRQ
  [0.1, 0.1, 0.1]
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
}

function draw() {
  let BACKGROUND_COLOR  = negative ? color('#ffffff') : color('#69479F');
  let LAYER_COLOR       = negative ? color('#69479F') : color('#ffffff');

  background(BACKGROUND_COLOR);
  strokeWeight(5);
  noFill();

  translate(windowWidth / 2, windowHeight / 2);

  let NOISE = PARAMS[0][0];   // 0.10 to 1.00
  let PACE  = PARAMS[0][1];   // 0.01 to 0.10
  let FREQ  = PARAMS[0][2];   // 0.00 to 0.00

  // let NOISE = (heartRate) < 100 ? 0 : map(heartRate, 100, 160, 0.1, 1)
  // let PACE = (heartRate) < 100 ? 0 : map(heartRate, 100, 160, 0.01, 0.1)
  // let FREQ = (heartRate) < 80 ? 0.1 : map(heartRate, 80, 160, 0, 1)

  // // every 10 above a hundred introduces the noise
  // // under 100, it should remain normal pulsing and stay circle

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