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
#define D14 14
#define D15 15
#define D16 16
#define D17 17
#define D18 18
#define D19 19
#define D20 20
#define D21 21
#define D22 22
#define D23 23
#define D24 24
#define D25 25
#define D26 26
#define D27 27
#define D28 28
#define D29 29
#define D30 30
#define D31 31
#define D32 32
#define D33 33
#define D34 34
#define D35 35
#define D36 36
#define D37 37
#define D38 38
#define D39 39
#define D40 40
#define D41 41
#define D42 42
#define D43 43
#define D44 44
#define D45 45
#define D46 46
#define D47 47
#define D48 48
#define D49 49
#define D50 50
#define D51 51
#define D52 52
#define D53 53
#define DIM 12

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
{0, 0},
{0, 0},
{0, 0},
{0, 0}
};

int test_trails[DIM][2] = {
{1, 5},
{1, 6},
{2, 4},
{3, 4},
{4, 5},
{4, 6},
{4, 10},
{4, 11},
{5, 8},
{5, 11},
{6, 7},
{6, 9}
};

int unique_trails[11] = {1,2,3,4,5,6,7,8,9,10,11};

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

void setup(){
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
  pinMode(D14, INPUT_PULLUP);
  pinMode(D15, INPUT_PULLUP);
  pinMode(D16, INPUT_PULLUP);
  pinMode(D17, INPUT_PULLUP);
  pinMode(D18, INPUT_PULLUP);
  pinMode(D19, INPUT_PULLUP);
  pinMode(D20, INPUT_PULLUP);
  pinMode(D21, INPUT_PULLUP);
  pinMode(D22, INPUT_PULLUP);
  pinMode(D23, INPUT_PULLUP);
  pinMode(D24, INPUT_PULLUP);
  pinMode(D25, INPUT_PULLUP);
  pinMode(D26, INPUT_PULLUP);
  pinMode(D27, INPUT_PULLUP);
  pinMode(D28, INPUT_PULLUP);
  pinMode(D29, INPUT_PULLUP);
  pinMode(D30, INPUT_PULLUP);
  pinMode(D31, INPUT_PULLUP);
  pinMode(D32, INPUT_PULLUP);
  pinMode(D33, INPUT_PULLUP);
  pinMode(D34, INPUT_PULLUP);
  pinMode(D35, INPUT_PULLUP);
  pinMode(D36, INPUT_PULLUP);
  pinMode(D37, INPUT_PULLUP);
  pinMode(D38, INPUT_PULLUP);
  pinMode(D39, INPUT_PULLUP);
  pinMode(D40, INPUT_PULLUP);
  pinMode(D41, INPUT_PULLUP);
  pinMode(D42, INPUT_PULLUP);
  pinMode(D43, INPUT_PULLUP);
  pinMode(D44, INPUT_PULLUP);
  pinMode(D45, INPUT_PULLUP);
  pinMode(D46, INPUT_PULLUP);
  pinMode(D47, INPUT_PULLUP);
  pinMode(D48, INPUT_PULLUP);
  pinMode(D49, INPUT_PULLUP);
  pinMode(D50, INPUT_PULLUP);
  pinMode(D51, INPUT_PULLUP);
  pinMode(D52, INPUT_PULLUP);
  pinMode(D53, INPUT_PULLUP);
}

void loop(){

  delay(500);

  Serial.println("Trails -> Digital Pins");
  for(int i; i < sizeof(unique_trails)/sizeof(unique_trails[0]); i++){
    Serial.print(unique_trails[i]);
    Serial.print(" -> ");
    Serial.print('D');
    Serial.println(i+2);
  }
  Serial.println();

  Serial.println("Ready?");
  Serial.read();

//-------------------------------------//

  pinMode(D2, OUTPUT);
  digitalWrite(D2, LOW);

  testPin(D6, 0);
  testPin(D7, 1);

  digitalWrite(D2, HIGH);
  pinMode(D2, INPUT_PULLUP);

//-------------------------------------//

  pinMode(D3, OUTPUT);
  digitalWrite(D3, LOW);

  testPin(D5, 2);

  digitalWrite(D3, HIGH);
  pinMode(D3, INPUT_PULLUP);

//-------------------------------------//

  pinMode(D4, OUTPUT);
  digitalWrite(D4, LOW);

  testPin(D5, 3);

  digitalWrite(D4, HIGH);
  pinMode(D4, INPUT_PULLUP);

//-------------------------------------//

  pinMode(D5, OUTPUT);
  digitalWrite(D5, LOW);

  testPin(D6, 4);
  testPin(D7, 5);
  testPin(D11, 6);
  testPin(D12, 7);

  digitalWrite(D5, HIGH);
  pinMode(D5, INPUT_PULLUP);

//-------------------------------------//

  pinMode(D6, OUTPUT);
  digitalWrite(D6, LOW);

  testPin(D9, 8);
  testPin(D12, 9);

  digitalWrite(D6, HIGH);
  pinMode(D6, INPUT_PULLUP);

//-------------------------------------//

  pinMode(D7, OUTPUT);
  digitalWrite(D7, LOW);

  testPin(D8, 10);
  testPin(D10, 11);

  digitalWrite(D7, HIGH);
  pinMode(D7, INPUT_PULLUP);

//-------------------------------------//

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

  Serial.println();

  while(1){
    delay(10);
  }
}