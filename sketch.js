let numPoints; // Points per circle for smoothness
let numLayers = 10;  // Number of radial layers (terrain depth)
let baseRadius; // Radius of the innermost circle
let layerSpacing = 12; // Spacing between layers
let timeFactor = 0.01; // Speed of animation

let slider, slider2, slider3, slider4;
let sliderr, sliderg, sliderb, sliderri, slidergi, sliderbi;

const SLIDER_HEIGHT = '30px';  // Constant for slider height

function createSliderWithStyle(min, max, value, step, positionX, positionY, width) {
  const slider = createSlider(min, max, value, step);
  slider.position(positionX, positionY);
  slider.style('width', width);
  slider.style('height', SLIDER_HEIGHT);
  return slider;
}

function createLabelWithStyle(text, positionX, positionY, width) {
  const label = createElement('label', text);
  label.attribute('type', 'text');
  label.position(positionX, positionY - 20);
  label.style('width', width);
  label.style('height', SLIDER_HEIGHT);
  label.style('color', 'white');  // Black text
  label.style('border', 'none');  // No border
  label.style('text-align', 'center');
  label.style('font-size', '20px');
  return label;
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  noFill();

  let sliderWidth = width * 0.8; // 80% of the canvas width for the sliders
  baseRadius = height * 0.13;

  // Create sliders with the helper function
  // Outer ring
  sliderr = createSliderWithStyle(0, 255, 100, 1, (width - sliderWidth) / 2, height - 50, sliderWidth / 3 - 10 + 'px');
  labelr = createLabelWithStyle('Red', (width - sliderWidth) / 2, height - 50, sliderWidth / 3 - 10 + 'px');

  sliderg = createSliderWithStyle(0, 255, 100, 1, (width - sliderWidth) / 2 + sliderWidth / 3, height - 50, sliderWidth / 3 - 10 + 'px');
  labelg = createLabelWithStyle('Green', (width - sliderWidth) / 2 + sliderWidth / 3, height - 50, sliderWidth / 3 - 10 + 'px');
  
  sliderb = createSliderWithStyle(0, 255, 100, 1, (width - sliderWidth) / 2 + (2 * sliderWidth) / 3, height - 50, sliderWidth / 3 - 10 + 'px');
  labelb = createLabelWithStyle('Blue', (width - sliderWidth) / 2 + (2 * sliderWidth) / 3, height - 50, sliderWidth / 3 - 10 + 'px');

  // Inner ring
  sliderri = createSliderWithStyle(0, 255, 100, 1, (width - sliderWidth) / 2, height - 100, sliderWidth / 3 - 10 + 'px');
  labelri = createLabelWithStyle('Inner Red', (width - sliderWidth) / 2, height - 100, sliderWidth / 3 - 10 + 'px');
  
  slidergi = createSliderWithStyle(0, 255, 100, 1, (width - sliderWidth) / 2 + sliderWidth / 3, height - 100, sliderWidth / 3 - 10 + 'px');
  labelgi = createLabelWithStyle('Inner Green', (width - sliderWidth) / 2 + sliderWidth / 3, height - 100, sliderWidth / 3 - 10 + 'px');
  
  sliderbi = createSliderWithStyle(0, 255, 100, 1, (width - sliderWidth) / 2 + (2 * sliderWidth) / 3, height - 100, sliderWidth / 3 - 10 + 'px');
  labelbi = createLabelWithStyle('Inner Blue', (width - sliderWidth) / 2 + (2 * sliderWidth) / 3, height - 100, sliderWidth / 3 - 10 + 'px');

  // # of points (polygon)
  slider2 = createSliderWithStyle(3, 50, 50, 1, (width - sliderWidth) / 2, height - 150, sliderWidth + 'px');
  createLabelWithStyle('Number of Points', (width - sliderWidth) / 2, height - 150, sliderWidth + 'px');
  
  // Speed
  slider3 = createSliderWithStyle(0.01, 0.1, 0.01, 0.001, (width - sliderWidth) / 2, height - 200, sliderWidth + 'px');
  createLabelWithStyle('Time Factor', (width - sliderWidth) / 2, height - 200, sliderWidth + 'px');
  
  // Distortion
  slider4 = createSliderWithStyle(0.1, 1.0, 0.01, 0.001, (width - sliderWidth) / 2, height - 250, sliderWidth + 'px');
  createLabelWithStyle('Noise Scale', (width - sliderWidth) / 2, height - 250, sliderWidth + 'px');
}

function draw() {
  background(20);
  translate(width / 2, height / 3); // Center the visualization

  numPoints = slider2.value();

  // Get the color values for the inner and outer color strokes
  let color1 = color(sliderri.value(), slidergi.value(), sliderbi.value()); // Inner color
  let color2 = color(sliderr.value(), sliderg.value(), sliderb.value()); // Outer color (can be different)

  strokeWeight(1.2);
  for (let layer = 0; layer < numLayers; layer++) {
    let radius = baseRadius + layer * layerSpacing; // Radius of the current layer
    let noiseScale = layer * slider4.value(); // Scale noise differently for each layer
    let colorFactor = map(layer, 0, numLayers, 0.0, 1.0); // Color gradient

    let lerpedColor = lerpColor(color1, color2, colorFactor);
    
    stroke(lerpedColor); // Gradient color

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
