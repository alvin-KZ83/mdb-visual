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

  // OUTER
  // Position the sliders centered horizontally
  sliderr = createSlider(0,255,100,1);
  sliderr.position((width - sliderWidth) / 2, height - 50);
  sliderr.style('width', sliderWidth / 3 - 10 + 'px');
  sliderr.style('height', '30px');  // Larger slider height for easier use

  // Position the sliders centered horizontally
  sliderg = createSlider(0,255,100,1);
  sliderg.position(10 + sliderWidth / 3 + (width - sliderWidth) / 2, height - 50);
  sliderg.style('width', sliderWidth / 3 - 10 + 'px');
  sliderg.style('height', '30px');  // Larger slider height for easier use

  // Position the sliders centered horizontally
  sliderb = createSlider(0,255,100,1);
  sliderb.position(15 + sliderWidth / 3 + sliderWidth / 3 + (width - sliderWidth) / 2, height - 50);
  sliderb.style('width', sliderWidth / 3 - 10 + 'px');
  sliderb.style('height', '30px');  // Larger slider height for easier use

  //INNER
  // Position the sliders centered horizontally
  sliderri = createSlider(0,255,100,1);
  sliderri.position((width - sliderWidth) / 2, height - 100);
  sliderri.style('width', sliderWidth / 3 - 10 + 'px');
  sliderri.style('height', '30px');  // Larger slider height for easier use

  // Position the sliders centered horizontally
  slidergi = createSlider(0,255,100,1);
  slidergi.position(10 + sliderWidth / 3 + (width - sliderWidth) / 2, height - 100);
  slidergi.style('width', sliderWidth / 3 - 10 + 'px');
  slidergi.style('height', '30px');  // Larger slider height for easier use

  // Position the sliders centered horizontally
  sliderbi = createSlider(0,255,100,1);
  sliderbi.position(15 + sliderWidth / 3 + sliderWidth / 3 + (width - sliderWidth) / 2, height - 100);
  sliderbi.style('width', sliderWidth / 3 - 10 + 'px');
  sliderbi.style('height', '30px');  // Larger slider height for easier use

  slider2 = createSlider(3, 50, 50, 1);
  slider2.position((width - sliderWidth) / 2, height - 150);
  slider2.style('width', sliderWidth + 'px');
  slider2.style('height', '30px');

  slider3 = createSlider(0.01, 0.1, 0.01, 0.001);
  slider3.position((width - sliderWidth) / 2, height - 200);
  slider3.style('width', sliderWidth + 'px');
  slider3.style('height', '30px');

  slider4 = createSlider(0.1, 1.0, 0.01, 0.001);
  slider4.position((width - sliderWidth) / 2, height - 250);
  slider4.style('width', sliderWidth + 'px');
  slider4.style('height', '30px');
  
}

function draw() {
  background(20);
  translate(width / 2, 1 * height / 3); // Center the visualization

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
