public class RGB {
  int r, g, b;
  
  public RGB(int r, int g, int b) {
    this.r = r;
    this.g = g;
    this.b = b;
  }
  
  public void draw_led(int x, int y) {
    fill(this.r, this.g, this.b);
    rect(x, y, LED_SQ_SIZE, LED_SQ_SIZE);
  }
}
