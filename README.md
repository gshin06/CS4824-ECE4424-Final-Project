
# CS4824-ECE4424-Final-Project
> Our testing data was not included as it contained numerous private mac addresses. If needed, please contact us for the data.
> Contributors: Daniel Shin (dshin26), Gabriel Shin (gshin06), Alex Lee (alexlee1017), Jack Timmins (jtimmins)
---
# Introduction
Every student on campus has at some point or another boarded the BT Transport bus only to find that its completely packed, despite the app saying otherwise. Bus drivers in the current system are required to manually keep track of current passengers, but this system is primitive and flawed. Human error can lead to invalid and incorrect data which brings harm to not only the BT system, but also the passengers who ride and utilize their services. In order to solve this problem, our team has recreated the results from the paper "Estimating Bus Cross-Sectional Flow Based on Machine Learning Algorithm Combined with Wi-Fi Probe Technology" [1] generated by utilizing machine learning to analyze wifi data in order to estimate the current number of passengers on a bus.

# Summary of the Original Paper
The original paper "Estimating Bus Cross-Sectional Flow Based on Machine Learning Algorithm Combined with Wi-Fi Probe Technology" by Ting-Zhao Chen, Yan-Yan Chen, and Jian-Hui Lai sought to create a machine algorithm that would estimate the amount of passengers inside a bus based on device wifi signals. This was done by placing 6 probes around the bus and estimating data received to predict bus capacity. However, a large portion of the paper primarily focused on determining which machine learning algorithm had the greatest accuracy. The team tested Random Forest, K-Nearest Neighbor, and Support Vector Machine. Each algorithm was fed the same feature vector: RRSI_AVG, RSSI_SUM, RSSI_ST, C_T, and M_AVG. These features are the average signal strength, the total sum of the signal strength, the standard deviation of the signal pool, the amount of times each signal was detected, and the average number of signals detected. The data was collected and converted into aforementioned vector by placing their 6 devices into a public bus and labelling the data manually by counting each passenger. This data was then fed into all 3 algorithms. The paper determined that Random Forest was the most accurate algorithm for the bus capacity problem. Additionally, they found that specifically for KNN, a K value of 8 was the most accurate.

# Our Method
The purpose of our project was to replicate the experiment conducted by the paper. However various changes were made to their methods. Additionally all software and hardware was developed aside from the esp-32 we used. First we instead analyzed and collected bluetooth signals over wifi. This was because our device with our developed system, probing wifi was not possible. We believed analyzing only bluetooth was acceptable as bluetooth signals would behave similarly to wifi. These signals were collected every 2 seconds and then the data was converted into bundles of 20 second intervals. This was because the component vector used by the paper analyzed in batches of times. Additionally, we changed the feature vector to instead break down C_T into 4 percentages of the time. Each C_T would record how many devices were found for a certain length of time. The first covering 0-5 seconds, the second covering 5-10 seconds, the third covering 10-15 seconds, and the last considered any duration of over 15 seconds. All other components were kept as close as possible to the paper. It is also important to note that our experiment contained only one esp-32, as one was sufficient to cover a radius of the car and outside of the car. The actual collection of the data was done by taking the esp-32 into a private car and driving a route similar to a bus. We varied the number of passengers in the vehicle and drove to densly populated areas. This data was then fed into 3 algorithms: KNN, RF, and SVM similarly to the paper. We then analyzed these results and compared them to the original paper. Additionally after data analysis we cross validated with a split of 20-80.

# Data Collection

# Data Preprocessing
In terms of data preprocessing, the initial data was sent from the esp32 as a json file containing the time of the ping, the MAC address, the signal strength, and the number of probed devices. This had to be converted to the 8 features to be used during the machine learning process. This was done by breaking the data into 20 second chunks and then calculating the features from the data inside each chunk. This was then formatted into a numpy array along side another array for the labels and passed to each machine learning algorithm

# Data Analysis
After feeding our preprocessed data from the esp-32 into Random Forest, K-Nearest Neighbor (We cross validated KNN), and Support Vector Machines, we found very similar results to the paper. We similarly found that Random Forest has the highest accuracy of 90%. As for SVM and KNN, our implementation found an accuracy rate of 80% for both consistently between different runs. However, it is important to note that our KNN did not have the same best K value of 8. Our data found that a K value of 5 or higher had an erroneously high accuracy among our data. We believe that this is due to our relatively small sample size. Due to different limitations and time constraints, we were only able to collect about 20 minutes of driving data.

Additionally, other factors of our experiment differed from the paper's. As mentioned before we based our system off of bluetooth signals only while the original paper parsed both bluetooth and wifi signals. This change was due to the hardware limitations of our esp-32. Additionally, we only used one esp-32. However, this was because we only needed one to cover the area of the vehicle we collected our data in and anymore could produce noise that wouldn't normally be found in a realistic implementation of our system. Finally, our component vector was slightly different from the paper's. The paper's description of their feature vector was slightly vague specifically about what C_T was. We interpreted it as the amount of time a certain mac address was detected in the system over the course of each 20 second block. We decided to further break this data point down to 4 different C_T which kept track of the number of devices detected for certain lengths of time. The first C_T keeping track of devices detected for 0-5 seconds, the second detecting 5-10 seconds, the third detecting 10-15, and the fourth detecting any over 15 seconds. We believed that this made the most sense in the context of the data and also could help our data be more accurate than the paper's. This would allow for a more definitive implementation of C_T and we believed that having separate metrics for each category would result in proportionately better results. For our random forest, we found an error rate of .10 which was slightly less than the paper's .1338. However once again this could be a result of our dataset.

Our KNN analysis can be seen here:
![image](https://github.com/gshin06/CS4824-ECE4424-Final-Project/assets/149714026/02e2248b-090f-4a33-a609-db16988fb71e)
As mentioned previously, we found that 5 was by far the best K value, but this was also because our system erroneously saw K values that were higher than 5 as 100% accuracy. We believe that this might have been a result of our dataset and our data collection process. In the future we hope to train our algorithm off a much higher varied data set and possibly within a real bus.

Here are the results of our code:
RF: ![image](https://github.com/gshin06/CS4824-ECE4424-Final-Project/assets/149714026/c008dcb5-3da2-4a76-b69c-04de65a5fb17)
SVM: ![image](https://github.com/gshin06/CS4824-ECE4424-Final-Project/assets/149714026/339eba6c-72ff-4733-a6d5-3115dd0c9946)
KNN (K=5): ![image](https://github.com/gshin06/CS4824-ECE4424-Final-Project/assets/149714026/93652c98-f991-455a-a692-c10e7c9a2287)

# Results
As mentioned in Data Analysis, our implementation showed very similar results to the paper's. However, we did find a slightly higher accuracy on our algorithms as shown above. KNN did show a 100% accuracy on K values above 5. This is most likely attributed to the small dataset with limited variety. Our results for RF and SVM were to be expected. More specifically for RF, we did find higher accuracy which we attribute to our higher dimensionality feature vector. 

# Limitations
As hinted at throughout this document, our team faced many limitations due to time constraints and the scope of the class. For our research, we were not able to collect data in an actual bus and had to conduct the research in a privately owned vehicle. This was to protect the privacy of other bus passengers. This also meant, we were not able to vary the passengers inside the car as frequently as a bus. Additionally, as mentioned previously, our probe was not able to detect wifi signals nor apple bluetooth signals. 

# Conclusion
Overall, our implementation was a successful recreation of the paper with a much more concise component vector. We believe that in a future application of this system, Random Forest should most definitely be used with our feature vector. This type of system could not only automate the capacity tracking system most bus drivers have to do, it can also be used to show each bus' capacity to passengers who can then plan their schedule around it. Finally, this system could also help bus companies plan optimized routes based on capacity throughout the day.

Link to the presentation: https://docs.google.com/presentation/d/1WHO-mUINIKCGxOV-QzWcXIXRl1-m361wblRSLyLf-tI/edit?usp=sharing

# Citations
[1] T.-Z. Chen, Y.-Y. Chen, and J.-H. Lai, “Estimating Bus Cross-Sectional Flow Based on Machine Learning Algorithm Combined with Wi-Fi Probe Technology,” \textit{Sensors}, vol. 21, no. 3, p. 844, Jan. 2021, doi: https://doi.org/10.3390/s21030844.
‌

BT archive
[2] “Data Archive,” \textit{ridebt.org}. https://ridebt.org/data-archive (accessed Oct. 25, 2023).
‌

Secondary wifi source if we use it. It has the real life trial.
[3] U. Mehmood, I. Moser, P. P. Jayaraman, and A. Banerjee, “Occupancy Estimation using WiFi: A Case Study for Counting Passengers on Busses,” \textit{2019 IEEE 5th World Forum on Internet of Things (WF-IoT)}, Apr. 2019, doi: https://doi.org/10.1109/wf-iot.2019.8767350.
‌

GIS Data
[4] “Town of Blacksburg GIS Data,” \textit{sites.google.com}. https://sites.google.com/vt.edu/townofblacksburggisdata/home‌


Weather data
[5] “Blacksburg, VA Weather History | Weather Underground,” \textit{www.wunderground.com}. https://www.wunderground.com/history/daily/us/va/blacksburg (accessed Oct. 25, 2023).
\end{document}
