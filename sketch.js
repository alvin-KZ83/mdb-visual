let numLayers = 10;
let baseRadius;

function updateValue(slider) {
  const valueSpan = document.getElementById(slider.id + '-value');
  valueSpan.textContent = slider.value;
}

function updateColorValue(input) {
  const hexColor = input.value;
  const r = parseInt(hexColor.substr(1, 2), 16);
  const g = parseInt(hexColor.substr(3, 2), 16);
  const b = parseInt(hexColor.substr(5, 2), 16);

  // Update the corresponding color value display
  document.getElementById(input.id + "-value").textContent = hexColor;

  // Optionally, store RGB values in variables for use in your drawing
  if (input.id === "outer-color") {
    window.outerRed = r;
    window.outerGreen = g;
    window.outerBlue = b;
  } else if (input.id === "inner-color") {
    window.innerRed = r;
    window.innerGreen = g;
    window.innerBlue = b;
  }

  console.log(`Color selected: ${hexColor} -> R: ${r}, G: ${g}, B: ${b}`);
}

function setup() {
  createCanvas(windowWidth, windowHeight / 2);
  noFill();
  baseRadius = width * 0.1;
}

function draw() {
  background(20);
  translate(width / 2, height / 2);

  // Use the RGB values stored in the window object
  const outerColor = color(window.outerRed || 100, window.outerGreen || 100, window.outerBlue || 100);
  const innerColor = color(window.innerRed || 100, window.innerGreen || 100, window.innerBlue || 100);

  const numPoints = parseInt(document.getElementById('num-points').value);
  const timeFactor = parseFloat(document.getElementById('time-factor').value);
  const noiseScale = parseFloat(document.getElementById('noise-scale').value);
  const thickness = parseFloat(document.getElementById('thickness').value);
  const spacing = parseInt(document.getElementById('spacing').value);

  strokeWeight(thickness);

  for (let layer = 0; layer < numLayers; layer++) {
    let radius = baseRadius + layer * spacing;
    let noiseOffsetScale = layer * noiseScale;
    let colorFactor = map(layer, 0, numLayers, 0, 1);
    let lerpedColor = lerpColor(innerColor, outerColor, colorFactor);

    stroke(lerpedColor);

    beginShape();
    for (let i = 0; i < numPoints; i++) {
      let angle = i * TWO_PI / numPoints;
      let noiseOffset = noise(
        cos(angle) * noiseOffsetScale,
        sin(angle) * noiseOffsetScale,
        frameCount * timeFactor
      );
      let r = radius + noiseOffset * 50;

      let x = r * cos(angle);
      let y = r * sin(angle);

      vertex(x, y);
    }
    endShape(CLOSE);
  }
}
