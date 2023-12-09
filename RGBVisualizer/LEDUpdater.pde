import websockets.*;

class LEDUpdater {
  WebsocketClient ws;
  
  String host;
  int port;
  
  int led_count;
  
  public LEDUpdater(PApplet parent, String host, int port, int led_count) {
    this.host = host;
    this.port = port;
    this.led_count = led_count;
    
    ws = new WebsocketClient(parent, "ws://" + host + ":" + port);  
  }
  
  void init() {
    JSONObject init_msg = new JSONObject();
    
    init_msg.setString("type", "setup-led-count");
    init_msg.setInt("content", this.led_count);
    
    ws.sendMessage(init_msg.toString());
  }

};
