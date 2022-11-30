#include <LiquidCrystal.h>
#include <EasyBuzzer.h>
#include <string.h>
#include <MFRC522.h>
#define actuador A1
//#define verde 
#define rojo A2
#define azul A3

String lectura = "0";
int este =5;

const int Trigger = A0;
const int Echo = 8;

const int pinBuzzer = A5;
const int tonos[] = {300};
const int countTonos = 1;

int puerta = 0;
int valor = 0;
int salida = 0;

float t; //timepo que demora en llegar el eco
float d; //distancia en centimetros

#define RST_PIN	9    //Pin 9 para el reset del RC522
#define SS_PIN	10   //Pin 10 para el SS (SDA) del RC522
MFRC522 mfrc522(SS_PIN, RST_PIN); ///Creamos el objeto para el RC522

LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

void setup() {
	Serial.begin(115200); //Iniciamos La comunicacion serial
  //Serial.begin(9600);
	SPI.begin();        //Iniciamos el Bus SPI
  lcd.begin(16,2);
	mfrc522.PCD_Init(); // Iniciamos el MFRC522
  pinMode(Trigger, OUTPUT); //pin como salida
  pinMode(Echo, INPUT);  //pin como entrada
  digitalWrite(Trigger, 0);
  
  salida = 3;

  EasyBuzzer.setPin(A5);
  pinMode(actuador,1);
  pinMode(A5,1);
  pinMode(A4,INPUT);
  pinMode(A3,1);
  pinMode(A2,1);
  pinMode(A1,1);
  lcd.print("Control de acceso");
}

byte ActualUID[4]; //almacenará el código del Tag leído
byte Usuario1[4]= {0x90, 0x5B, 0xF8, 0x79} ; //código del usuario 1
byte Usuario2[4]= {0x04, 0xEA, 0x0D, 0x85} ; //código del usuario 2

void loop() {
String lectura;
int este=5;

   while (Serial.available()){
    char entrada = Serial.read();
    lectura = lectura + entrada;
    lectura.trim();
    este = lectura.toInt();
    lectura = "";
   }

switch (este){
case 1:
  lcd.clear();
  lcd.print("MODO AUTO");
  delay(2000);
  lcd.clear();
  Automatico();
  break;

case 2:
  lcd.clear();
  lcd.print("MODO MANUAL");
  delay(2000);
  lcd.clear();
  manual();
  break;

case 3: 
      digitalWrite(actuador, 0);
      digitalWrite(azul,1);
      digitalWrite(rojo,1);
      tone(pinBuzzer, 250);
      lcd.clear();
      lcd.print("Puerta Abierta");
      break;

case 4:
    digitalWrite(actuador, 1);
    digitalWrite(rojo,1);
    tone(pinBuzzer, 50);
      lcd.clear();
      lcd.print("Puerta Cerrada");
      break;

case 5:
  //SPI.attachInterrupt();
  digitalWrite(9,0);
  digitalWrite(10,0);
  datos();

}
}


void manual()
{
  int sel =2;
  lcd.clear();
  lcd.print("MODO MANUAL");


}
void Automatico()
{
 int hola = 1;
  while (hola ==1){
       while (Serial.available()){
    char entrada = Serial.read();
    lectura = lectura + entrada;
    lectura.trim();
    este = lectura.toInt();
    lectura = "";
    hola = este;
   }
  
  digitalWrite(rojo,0);
  puerta = 0;
  RFID();
  sensor();
  tranca();
	if (puerta == 1){
    lcd.clear();
    lcd.print("Puerta Abierta");
    tone(pinBuzzer, 250);
    digitalWrite(actuador,1);
    digitalWrite(azul,1);
    digitalWrite(rojo,1);
    delay(3000);
    noTone(pinBuzzer);
    digitalWrite(azul,0);
    digitalWrite(rojo,0);
    digitalWrite(actuador,0);
    //Distancia();
  }
  
  if (puerta == 2)
  {
    digitalWrite(azul,0);
    lcd.clear();
    lcd.print("Acceso Denegado");
    tone(pinBuzzer, 50);
    digitalWrite(rojo,1);
    delay(3000);
    noTone(pinBuzzer);
    digitalWrite(rojo,0);
    //Distancia();
  }
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("   Esperando");
  lcd.setCursor(0, 1);
  lcd.print("    Tarjeta");
  digitalWrite(azul,1);
  datos();
}
}

//Función para comparar dos vectores
 boolean compareArray(byte array1[],byte array2[])
{
  if(array1[0] != array2[0])return(false);
  if(array1[1] != array2[1])return(false);
  if(array1[2] != array2[2])return(false);
  if(array1[3] != array2[3])return(false);
  return(true);
}
void RFID()
{
	if ( mfrc522.PICC_IsNewCardPresent()) 
        {  
  		//Seleccionamos una tarjeta
            if ( mfrc522.PICC_ReadCardSerial()) 
            {
                  // Enviamos serialemente su UID
                  //Serial.print(F("Card UID:"));
                  for (byte i = 0; i < mfrc522.uid.size; i++) {
                          //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
                          //Serial.print(mfrc522.uid.uidByte[i], HEX);   
                          ActualUID[i]=mfrc522.uid.uidByte[i];          
                  }              
                  //comparamos los UID para determinar si es uno de nuestros usuarios  
                  if(compareArray(ActualUID,Usuario1))
                    puerta = 1;
                  else if(compareArray(ActualUID,Usuario2))
                    puerta = 2;
                 // else 
                   // lcd.println("Acceso denegado...");
                  
                  // Terminamos la lectura de la tarjeta tarjeta  actual
                  mfrc522.PICC_HaltA();
              
            }
      
	}

}
void tranca() 
{
if(d<10) 
{
tone(pinBuzzer, 250);
digitalWrite(actuador,1);
digitalWrite(azul,1);
digitalWrite(rojo,1);
lcd.clear();
lcd.print(" Puerta Abierta");
delay(5000);
digitalWrite(azul,0);
digitalWrite(rojo,0);
digitalWrite(actuador,0);
noTone(pinBuzzer);
}
}

void sensor(){ //lecutra HC-04
{
  digitalWrite(Trigger, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(Trigger, LOW);
  t = pulseIn(Echo, HIGH); //obtenemos el ancho del pulso
  d = t/59;             //escalamos el tiempo a una distancia en cm
  delay(100);          //Hacemos una pausa de 100ms
  }

}

void datos() {
  int act = digitalRead(actuador);
  sensor();
  Serial.print(d);
  Serial.print(",");
  Serial.println(act);

}