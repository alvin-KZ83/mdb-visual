let numLayers = 10;
let baseRadius;

function updateValue(slider) {
  const valueSpan = document.getElementById(slider.id + '-value');
  valueSpan.textContent = slider.value;
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  noFill();
  baseRadius = width * 0.06;
}

function draw() {
  background(20);
  translate(width / 2, height / 2);

  // Access slider values
  const outerRed = parseInt(document.getElementById('outer-red').value);
  const outerGreen = parseInt(document.getElementById('outer-green').value);
  const outerBlue = parseInt(document.getElementById('outer-blue').value);

  const innerRed = parseInt(document.getElementById('inner-red').value);
  const innerGreen = parseInt(document.getElementById('inner-green').value);
  const innerBlue = parseInt(document.getElementById('inner-blue').value);

  const numPoints = parseInt(document.getElementById('num-points').value);
  const timeFactor = parseFloat(document.getElementById('time-factor').value);
  const noiseScale = parseFloat(document.getElementById('noise-scale').value);
  const thickness = parseFloat(document.getElementById('thickness').value);
  const spacing = parseInt(document.getElementById('spacing').value);

  let color1 = color(innerRed, innerGreen, innerBlue);
  let color2 = color(outerRed, outerGreen, outerBlue);

  strokeWeight(thickness);
  for (let layer = 0; layer < numLayers; layer++) {
    let radius = baseRadius + layer * spacing;
    let noiseOffsetScale = layer * noiseScale;
    let colorFactor = map(layer, 0, numLayers, 0, 1);
    let lerpedColor = lerpColor(color1, color2, colorFactor);

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
