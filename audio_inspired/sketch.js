let numPoints; // Points per circle for smoothness
let numLayers = 10;  // Number of radial layers (terrain depth)
let baseRadius; // Radius of the innermost circle
let layerSpacing = 12; // Spacing between layers
let timeFactor = 0.01; // Speed of animation

let slider;
let slider2;
let slider3;

function setup() {
  createCanvas(windowWidth, windowHeight);
  noFill();

  // Calculate slider widths dynamically for mobile-friendliness
  let sliderWidth = width * 0.8; // 80% of the canvas width for the sliders

  baseRadius = height * 0.13;

  // Position the sliders centered horizontally
  slider = createSlider(1, 5, 3, 1);
  slider.position((width - sliderWidth) / 2, height - 80);
  slider.style('width', sliderWidth + 'px');
  slider.style('height', '50px');  // Larger slider height for easier use

  slider2 = createSlider(3, 50, 50, 1);
  slider2.position((width - sliderWidth) / 2, height - 120);
  slider2.style('width', sliderWidth + 'px');
  slider2.style('height', '50px');

  slider3 = createSlider(0.01, 0.3, 0.01, 0.001);
  slider3.position((width - sliderWidth) / 2, height - 160);
  slider3.style('width', sliderWidth + 'px');
  slider3.style('height', '50px');

  slider4 = createSlider(0.1, 1.0, 0.01, 0.01);
  slider4.position((width - sliderWidth) / 2, height - 200);
  slider4.style('width', sliderWidth + 'px');
  slider4.style('height', '50px');
}

function draw() {
  background(20);
  translate(width / 2, 1.1 * height / 3); // Center the visualization

  let sliderValue = slider.value(); // Value will be 1, 2, 3, 4, or 5
  numPoints = slider2.value();

  strokeWeight(1.2);
  for (let layer = 0; layer < numLayers; layer++) {
    let radius = baseRadius + layer * layerSpacing; // Radius of the current layer
    let noiseScale = layer * slider4.value(); // Scale noise differently for each layer
    let colorFactor = map(layer, 0, numLayers, 100, 255); // Color gradient
    
    if (sliderValue == 1) {
      stroke(colorFactor, 100, 100); // Gradient color
    }
    else if (sliderValue == 2) {
      stroke(colorFactor, 200, 100); // Gradient color
    }
    else if (sliderValue == 3) {
      stroke(100, colorFactor, 100); // Gradient color
    }
    else if (sliderValue == 4) {
      stroke(100, 200, colorFactor); // Gradient color
    }
    else if (sliderValue == 5) {
      stroke(100, 100, colorFactor); // Gradient color
    }

    beginShape();
    for (let i = 0; i < numPoints; i++) {
      let angle = i * TWO_PI / numPoints; // Angle of the current point


      let noiseOffset = noise(
        cos(angle) * noiseScale,
        sin(angle) * noiseScale,
        frameCount * slider3.value()
      ); // Noise for each point in the circle


      let r = radius + noiseOffset * 50; // Radius with terrain variation
      
      let x = r * cos(angle); // Polar to Cartesian
      let y = r * sin(angle);
      
      vertex(x, y); // Plot the point
    }
    endShape(CLOSE);
  }
}
