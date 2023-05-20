#define MAX_TRAILS 20
#define D2 2
#define D3 3
#define D4 4
#define D5 5
#define D6 6
#define D7 7
#define D8 8
#define D9 9
#define D10 10
#define D11 11
#define D12 12
#define D13 13
#define DIM 9

int cont = 0;

int marker[DIM][2] = {
  {0, 0},
  {0, 0},
  {0, 0},
  {0, 0},
  {0, 0},
  {0, 0},
  {0, 0},
  {0, 0},
  {0, 0}
};

int test_trails[DIM][2] = {
    {1, 3},
    {1, 5},
    {1, 7},
    {2, 3},
    {2, 5},
    {2, 6},
    {3, 5},
    {3, 6},
    {3, 7}
};

int testPin(int pin, int pos){
  if (!digitalRead(pin)){
    while(1){
      if(marker[cont][0]==0 && marker[cont][1]==0){
        marker[cont][0] = test_trails[pos][0];
        marker[cont][1] = test_trails[pos][1];
        cont++;
        break;
      }else{
        cont++;
      }
    }
  }
}

void finish(){
  delay(10);
  finish();
}

void setup() {
  Serial.begin(115200);
  pinMode(D2, INPUT_PULLUP);
  pinMode(D3, INPUT_PULLUP);
  pinMode(D4, INPUT_PULLUP);
  pinMode(D5, INPUT_PULLUP);
  pinMode(D6, INPUT_PULLUP);
  pinMode(D7, INPUT_PULLUP);
  pinMode(D8, INPUT_PULLUP);
  pinMode(D9, INPUT_PULLUP);
  pinMode(D10, INPUT_PULLUP);
  pinMode(D11, INPUT_PULLUP);
  pinMode(D12, INPUT_PULLUP);
  pinMode(D13, INPUT_PULLUP);
}

void loop() {
  
  delay(1000);

  //D2 -> 1
  //D3 -> 2
  //D4 -> 3
  //D5 -> 5
  //D6 -> 6
  //D7 -> 7

  //----------------------------------------------------------------------//

  pinMode(D2, OUTPUT);
  digitalWrite(D2, LOW);

  testPin(D4, 0);
  testPin(D5, 1);
  testPin(D7, 2);

  digitalWrite(D2, HIGH);
  pinMode(D2, INPUT_PULLUP);

  //----------------------------------------------------------------------//

  pinMode(D3, OUTPUT);
  digitalWrite(D3, LOW);

  testPin(D4, 3);
  testPin(D5, 4);
  testPin(D6, 5);

  digitalWrite(D3, HIGH);
  pinMode(D3, INPUT_PULLUP);

  //----------------------------------------------------------------------//

  pinMode(D4, OUTPUT);
  digitalWrite(D4, LOW);

  testPin(D5, 6);
  testPin(D6, 7);
  testPin(D7, 8);

  digitalWrite(D3, HIGH);
  pinMode(D4, INPUT_PULLUP);

  //----------------------------------------------------------------------//

  if(cont==0){
    Serial.println("No shorts!");
  }else{
    Serial.println("Shorts founds:");
    for(int x=0; x<cont; x++){
      Serial.print("Trails ");
      for(int y=0; y<2; y++){
        Serial.print(marker[x][y]);
        if(y==0){
          Serial.print(" and ");
        }
      }
      Serial.println();
    }
  }

  finish();

}
