// How many LEDs
final int LED_COUNT = 900;

// Displayed along how many rows
final int ROWS = 9;

// Size of the LED.
final int LED_SQ_SIZE = 10;

// Distance between each LED X, Y
final int X_INC = 12;
final int Y_INC = 12;
final int X_PAD = 20;
final int Y_PAD = 20;

// Websocket config
final String ws_host = "127.0.0.1";
final int ws_port = 9090;


RGB[] leds = new RGB[LED_COUNT];

LEDUpdater updater;


// Calculates the width of the window determined by the setup constants.
int calculate_win_width() {
  int window_width = 0;
  
  int led_per_row = LED_COUNT/ROWS;

  // Add the padding on left & right side.
  window_width += X_PAD * 2;
  
  // Add the LED's width.
  window_width += (LED_SQ_SIZE * led_per_row);
  
  // Add the spacing between LEDs.
  window_width += ( (X_INC - LED_SQ_SIZE) * led_per_row );
  
  return window_width;
}

int calculate_win_height() {
  int window_height = 0;
  
  // Add the top & bottom padding
  window_height += Y_PAD * 2;
  
  // Add the LED's height.
  window_height += (LED_SQ_SIZE * ROWS);
  
  // Add the spacing between LEDs.
  window_height += ( (Y_INC - LED_SQ_SIZE) * ROWS );

  return window_height;
}

// Setup the LEDS, and window.
void setup() {  
  RGB STARTCOLOR = new RGB(255, 0, 255);
  
  // Setup window.
  size(200, 200);
  windowTitle("LED Simulator V1.0");

  // Resize with appropriate sizing.
  int win_width = calculate_win_width();
  int win_height = calculate_win_height();
  
  windowResize(win_width, win_height);
  

  // Initialize the LEDS.
  for (int i = 0; i < LED_COUNT; i++) {
    leds[i] = new RGB(STARTCOLOR.r, STARTCOLOR.g, STARTCOLOR.b); 
  }
  
  updater = new LEDUpdater(this, ws_host, ws_port, leds);
  updater.init();
}

void draw_leds() {
  int led_per_row = LED_COUNT/ROWS;
  
  int led_idx = 0;

  int y = Y_PAD;
  int x = X_PAD;
  
  for (int i = 0; i < ROWS; i++) {
    for (int j = 0; j < led_per_row; j++) {
      RGB led = leds[led_idx];
      led_idx ++;
      
      led.draw_led(x, y);
      
      // Increment x to stop overlap.
      x += X_INC;
    }
    y += Y_INC;
    x = X_PAD;
  }
}


void draw() {
  background(200, 200, 200);  // Make background white.
  draw_leds();
  updater.update_leds();
  delay(100);
}


void webSocketEvent(String msg) {
  updater.message_handler(msg);  
}
