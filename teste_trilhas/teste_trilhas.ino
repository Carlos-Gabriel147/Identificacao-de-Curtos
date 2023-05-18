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
#define D12 1
#define D13 13
#define DIM 9

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

void setup() {
  Serial.begin(115200);
  pinMode(D2, INPUT);
  pinMode(D3, INPUT);
  pinMode(D4, INPUT);
  pinMode(D5, INPUT);
  pinMode(D6, INPUT);
  pinMode(D7, INPUT);
  pinMode(D8, INPUT);
  pinMode(D9, INPUT);
  pinMode(D10, INPUT);
  pinMode(D11, INPUT);
  pinMode(D12, INPUT);
  pinMode(D13, INPUT);
}

void loop() {
  int i = 0;
  int cont = 0;
  delay(3000);

  //--------------------Check 1----------------------//

  pinMode(D2, OUTPUT);
  pinMode(D3, INPUT);
  pinMode(D4, INPUT);
  pinMode(D5, INPUT);
  digitalWrite(D2, HIGH);

  if (digitalRead(D3)){
    while(1){
      if(marker[i][0]==0 && marker[i][1]==0){
        marker[i][0] = test_trails[0][0];
        marker[i][1] = test_trails[0][1];
        cont++;
        i++;
        break;
      }else{
        i++;
      }
    }
  }

  if (digitalRead(D4)){
    while(1){
      if(marker[i][0]==0 && marker[i][1]==0){
        marker[i][0] = test_trails[1][0];
        marker[i][1] = test_trails[1][1];
        cont++;
        i++;
        break;
      }else{
        i++;
      }
    }
  }

  if (digitalRead(D5)){
    while(1){
      if(marker[i][0]==0 && marker[i][1]==0){
        marker[i][0] = test_trails[2][0];
        marker[i][1] = test_trails[2][1];
        cont++;
        i++;
        break;
      }else{
        i++;
      }
    }
  }

  digitalWrite(D2, LOW);

  pinMode(D2, INPUT);
  pinMode(D3, OUTPUT);
  pinMode(D4, INPUT);
  pinMode(D5, INPUT);
  digitalWrite(D3, HIGH);

  if (digitalRead(D2)){
    while(1){
      if(marker[i][0]==0 && marker[i][1]==0){
        marker[i][0] = test_trails[3][0];
        marker[i][1] = test_trails[3][1];
        cont++;
        i++;
        break;
      }else{
        i++;
      }
    }
  }

  if (digitalRead(D4)){
    while(1){
      if(marker[i][0]==0 && marker[i][1]==0){
        marker[i][0] = test_trails[4][0];
        marker[i][1] = test_trails[4][1];
        cont++;
        i++;
        break;
      }else{
        i++;
      }
    }
  }

  if (digitalRead(D5)){
    while(1){
      if(marker[i][0]==0 && marker[i][1]==0){
        marker[i][0] = test_trails[5][0];
        marker[i][1] = test_trails[5][1];
        cont++;
        i++;
        break;
      }else{
        i++;
      }
    }
  }

  if(cont==0){
    Serial.println("No short!");
  }else{
    Serial.println("Short found:");
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

  delay(999999);

}
