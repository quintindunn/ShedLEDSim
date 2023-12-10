import websockets.*;

class LEDUpdater {
  WebsocketClient ws;
  
  String host;
  int port;
  
  int led_count;
  
  RGB[] LEDs;
  
  public LEDUpdater(PApplet parent, String host, int port, RGB[] LEDs) {
    this.host = host;
    this.port = port;
    
    this.LEDs = LEDs;
    this.led_count = LEDs.length;
    
    
    ws = new WebsocketClient(parent, "ws://" + host + ":" + port);  
  }
  
  void init() {
    // Send a packet to the websocket server containing the amount of LEDs to register.
    JSONObject init_msg = new JSONObject();
    
    init_msg.setString("type", "setup-led-count");
    init_msg.setInt("content", this.led_count);
    
    ws.sendMessage(init_msg.toString());
  }
  
  void update_leds() {
    JSONObject update_msg = new JSONObject();
    update_msg.setString("type", "update-display");
    ws.sendMessage(update_msg.toString());
  }
  
  void update_display() {
    // Sends a packet to the websocket server for it to return all of the LEDs.

    JSONObject update_msg = new JSONObject();
    update_msg.setString("type", "dump-leds");
    
    ws.sendMessage(update_msg.toString());
  }
  
  void update_mode(String new_mode) {
    JSONObject mode_msg = new JSONObject();
    mode_msg.setString("type", "update-mode");
    mode_msg.setString("content", new_mode);
    
    ws.sendMessage(mode_msg.toString());
  }
  
  void led_dump_handler(JSONObject message) {
    // Parses the JSON sent and converts it into a RGB array.
    JSONArray raw_LEDs = parseJSONArray(message.getString("content"));
    RGB[] LEDs = new RGB[raw_LEDs.size()];
      
    for (int i = 0; i < raw_LEDs.size(); i++) {
        JSONArray LED = raw_LEDs.getJSONArray(i);
        int[] LED_values = LED.toIntArray();
 
        RGB new_led = new RGB(LED_values[0], LED_values[1], LED_values[2]);
        LEDs[i] = new_led;
    }
    
    // Copy the local leds array to the global leds array.
    
    if (leds.length != this.LEDs.length)
      println("Error: Length of LEDs recieved != defined LEDs");
    
    for (int i = 0; i < leds.length; i++) {
      this.LEDs[i] = LEDs[i]; 
    }
  }
  
  void message_handler(String msg) {
    JSONObject message = parseJSONObject(msg);
    
    String msg_type = message.getString("type");

    switch (msg_type) {
       case "connection-confirmed":
         System.out.println("Successfully connected to websocket");
         break;
       case "led-strip-initialized":
         System.out.println("Successfully intialized LEDStrip");
         break;
       case "led-dump":
         led_dump_handler(message);
         break;
    }
  }
};
