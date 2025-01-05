# Parking Sensor

### Initial phase
A system similar to the parking sensor found in most vehicles was developed for this project. A circuit was built with Raspberry Pi Pico as the microcontroller, HC-SR04 ultrasonic distance sensor, 7 LEDs, 2 buzzers, and a sound sensor. The purpose of this developed circuit is to notify the user how near the object is with the help of LEDs and the buzzer when the distance sensor detects an object is becoming near. The second buzzer and the sound sensor were added to the circuit to provide reliability, and their purposes will be explained in detail later in this report.  

**The circuit:**  
[Click to see the image of the circuit.](images/circuit.png)  
[Click to see the video of the circuit.](images/circuit.mp4)

### Identifying Fault Scenarios  
Aiming to gain a deeper understanding of the various risks and vulnerabilities that the embedded system being built may encounter, two dangerous scenarios that could affect the circuit was determined. These scenarios encompass a wide range of potential issues that could affect the operation of the project. While considering these scenarios, it was assumed that this system would be used in a real vehicle.  

**List and descriptions of the scenarios:**  
1. The distance sensor is malfunctioning and not operational.  
*If the distance sensor does not operate, it means that the entire circuit has lost its purpose and is now unusable. In this scenario, the issue lies solely with the distance sensor, and all other components are functioning as expected.*

2. The main buzzer (or LEDs and the main buzzer) is malfunctioning and not operational.  
*This is the most dangerous scenario that could occur. In this scenario, the issue lies solely with the main buzzer (or LEDs and the main buzzer, both), and the distance sensor is functioning as expected.*

### Developing Fault Tolerance Strategies  

**Fault tolerance mechanism of scenario 1:**  
This scenario is when the distance sensor does not operate, but all other components operate as they should. What makes this situation dangerous is that the white light is on, and the circuit is shown to be operating, but the system misleads the driver based on the wrong data the sensor generates. 

First, it was examined how the distance sensor behaves in cases where it is not operating, such as not receiving enough power or not having the trig or echo cables connected. As a result of the examinations, it was observed that the distance sensor generates negative values. Therefore, how the circuit will behave in cases where negative values come from the distance sensor was developed in the code. In this case, the two red LEDs will flash quickly while the buzzer will beep quickly. Thus, the driver will be aware of the fault in the system and will consider it.  

If the question of why a spare distance sensor is not selected for this situation instead of such a warning mechanism is asked, the answer is that it will increase the cost of the system. While small extra components such as a backup buzzer do not increase the cost much, the backup distance sensor will increase the cost a lot.  

**Fault tolerance mechanism of scenario 2:**  
This scenario is when the buzzer is malfunctioning and not operating. The other components operate as they should. If the question of how the malfunctioning of the buzzer can be a bigger problem than the malfunctioning of the distance sensor in this system is asked, the answer is that the buzzer is the most important component. When parking, drivers generally prefer to park by looking back and listening to the beep sound without looking at the digital display (LEDs). If there is no beep sound, they may continue driving back even if they observe back themself, thinking that the distance is still far.  

Therefore, a mechanism was carefully developed for the buzzer malfunction both in the code and in the circuit. A sound sensor that stands very close to the main buzzer was added to the circuit and a backup buzzer was also added. As can be easily observed in the code, the sound sensor constantly listens to the main buzzer with analogue data. However, it does this listening when the distance is below 30 cm because the buzzer does not sound if the distance is above 30 cm. If the buzzer still does not make a sound when the distance is below 30 cm, the sound sensor detects this and immediately activates the backup buzzer, thus ensuring that there is a working buzzer in this circuit.  
