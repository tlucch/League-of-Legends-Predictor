# League of Legends Predictor V1.0.0

## Introduction
This projects aim is to create a classification model to predict the outcome of league of legends games using info from the minute 14 of the game.
Why minute 14? For the people who don't know much about the game, this is the minute in which tower plates (a feature of the game) fall, and this particular event marks the end of the early games and the start of the middle game. So the real aim of this model is to predict the outcome of a League of LEgends game using as input the early game performance of the team

To achive this we have to follow the following steps:

* `Data Collection`
* `Feature Selection`
* `Model Testing`


## Data Collection

In order to get the data we must connect to the Riot API, more specifically to the "/lol/match/v5/matches/{matchId}/timeline" Riot API. With this API we can access to the info of every player minute by minute. This means we can get info from and up to the minute 14 of the game.

Although we can gather lots of information from this API, I decided to get the following parameters for each team:

* **Gold**: Total gold generated by the team
* **Level**: Each player has it's own level, so I decided to get the averge level of the team.
* **Minons**: Minions are non-player characters (NPCs) that spawn from each team’s base and gives you gold when you kill them. So the total amount amount of minions killed by the team
* **Jungle_minions**: Other NPCs that, unlike minions, dont belong to a team. They also give gold when killed and other temporary benefits. So the total amount amount killed by the team
* **Kills**: The total players killed by the team
* **Deaths**: The total deaths of the team
* **Assists**: The total assists in a kill of the team
* **Towers**: Towers are structures that need to get destroyed in orther to win the game. This parameter count the amount of tower broken by the team
* **Plates**: Plates are a structure that is protects the towers that when broken it give gold. This parameter count the amount of plates destroyed by the team
* **Dragons**: A Dragon is a neutral and difficult to kill NPC that gives permantent benefits to the team that kills it. Total amount killed by a team
* **Herald**: Another neutral and difficult to kill NPC that helps you to destroy enemy towers and plates. Total amount killed by a team
* **Sight_wards**: A ward is an object that when placed on the map it gives visiility of that zone. Sight Wards are a kind of ward. Total amount placed by a team
* **Control_wards**: Another kind of ward. Total amount placed by a team
* **Gold_diff**: The gold difference between each team. If your team has more gold the result is positive, otherwise its negative.
* **Win**: If team won at the end = 1, otherwise = 0

For this project I decided to use the info of the last 50 games played by the top 100 Korea players. To get this top 100 players I scrapped the League of Graph Korea ranking (League of Graphs is a web that shows different League of Legends Stats).

> **Note**
> The code for both the scarping and the data collection can be found in the `API-info-colector.py` file.

## Feature Selection
Although we extracted 13 different features, maybe not all of them are really influence in the outcome of the game. Thats why, before training and testing our models we have to select our features. Using the data extracted from the 50 last matches of the top 100 Korea players, which can be found in the `KR-History.xlsx` excel file, a correlation matrix was made, which showed the following results:

<br />
<p align = "center">
  <img src = "Images/Correlation Heatmap.png" width = 900>
</p>
<br />

Nice! We can see lots of interesting variables correlations between different variables. But our target variable is "Win", so lets see our correlations specifilacy using our "Win" variable:

<br />
<p align = "center">
  <img src = "Images/Win Correlation Heatmap.png" width = 500>
</p>
<br />

So now we can see our most significant variables are: `Gold_diff`, `Gold`, `Level`, `Kills`, `Deaths`, `Towers` and `Assists`, while `Sight_wards`, `Control_Wards` and `Plates` seem to how almost no impact in the game outcome. So, in conclusion, we can test our models using our original DataFrame with all our features and a reduced DataFrame withouth `Sight_wards`, `Control_Wards` and `Plates`.

## Model Testing
> **Note**
> The code for all the tests can be found in the `classification-models-testing.ipynb` file/notebook

Now that we know our features, we can start training and testing our models. For this project I decided to test 4 well known classification algorithm:

* `Logistic Regression`
* `Decision Tree`
* `Random Forest`
* `Support Vector Machine`

But before testing and analyzing our models, the first thing we need to do is splitour data into training and testing. For this particular case I decided to use the 33% testing split. Now yes, lets go to the fun part!

### Logistic Regression Original DF

Of course, when we speak about classification models the first thing that comes to our mind is "Logistic Regression", so thats what we did! 
First, the model was trained using the original dataframe with the following results:


****CLASSIFICATION REPORT - TRAINING DATA****
```` 
              precision    recall  f1-score   support

           0     0.7963    0.7968    0.7965      1673
           1     0.7944    0.7940    0.7942      1655

    accuracy                         0.7954      3328
   macro avg     0.7954    0.7954    0.7954      3328
weighted avg     0.7954    0.7954    0.7954      3328
````
****CLASSIFICATION REPORT - TEST DATA****
```` 
              precision    recall  f1-score   support

           0     0.8157    0.8187    0.8172       811
           1     0.8220    0.8191    0.8205       829

    accuracy                         0.8189      1640
   macro avg     0.8189    0.8189    0.8189      1640
weighted avg     0.8189    0.8189    0.8189      1640 
```` 

****CONFUSION MATRIX AND ROC-AUC VISUALIZATION****

<br />
<p align = "left">
  <img src = "Images/LogReg Original.png" width = 800>
</p>
<br />

OMG! What an excellent start! We got a recall of 80% recall on the train data and a 82% recall on the test data, which means our model is predicting 82% of the results correctly. In addition, the ROC-AUC curve looks excelent, it seems we have no over or underfitting. So now, lets pass see how this model performs with the reduced DataFrame.

### Logistic Regression Reduced DF

****CLASSIFICATION REPORT - TRAINING DATA****
```` 
              precision    recall  f1-score   support

           0     0.8002    0.7998    0.8000      1673
           1     0.7977    0.7982    0.7979      1655

    accuracy                         0.7990      3328
   macro avg     0.7990    0.7990    0.7990      3328
weighted avg     0.7990    0.7990    0.7990      3328
```` 
****CLASSIFICATION REPORT - TEST DATA****
```` 
              precision    recall  f1-score   support

           0     0.8156    0.8126    0.8141       811
           1     0.8173    0.8203    0.8188       829

    accuracy                         0.8165      1640
   macro avg     0.8165    0.8164    0.8164      1640
weighted avg     0.8165    0.8165    0.8165      1640
```` 
****CONFUSION MATRIX AND ROC-AUC VISUALIZATION****

<br />
<p align = "left">
  <img src = "Images/LogReg Reduced.png" width = 800>
</p>
<br />

Wow! This results are also awesome! In comparison to the original DataFrame Looks like it did a it better with the training set and a bit worse with the test data. Nevertheless, the diference is minimum, such that, when rounded, the training data got an 80% recall and the test an 82%, the same as the original data.

### Decision Tree Original DF

The next model we used is "Decsision Tree". Using the original DataFrame, we got the following results:

****CLASSIFICATION REPORT - TRAINING DATA****
````
              precision    recall  f1-score   support

           0     1.0000    1.0000    1.0000      1673
           1     1.0000    1.0000    1.0000      1655

    accuracy                         1.0000      3328
   macro avg     1.0000    1.0000    1.0000      3328
weighted avg     1.0000    1.0000    1.0000      3328
````
****CLASSIFICATION REPORT - TEST DATA****
````
              precision    recall  f1-score   support

           0     0.7484    0.7263    0.7372       811
           1     0.7397    0.7612    0.7503       829

    accuracy                         0.7439      1640
   macro avg     0.7441    0.7437    0.7437      1640
weighted avg     0.7440    0.7439    0.7438      1640
````
****CONFUSION MATRIX AND ROC-AUC VISUALIZATION****

<br />
<p align = "left">
  <img src = "Images/Tree Original.png" width = 800>
</p>
<br />

Well, it seems this model perfoms worst than the previous one as we got a 74% recall. Nevertheless, this is still an awesome result! But we want to stick with our best model. So... Im very sorry Decision Tree, but today is not you day :(

### Decision Tree Reduced DF
Lets see how it does with the reduced DataFrame.

****CLASSIFICATION REPORT - TRAINING DATA****
````
              precision    recall  f1-score   support

           0     1.0000    1.0000    1.0000      1673
           1     1.0000    1.0000    1.0000      1655

    accuracy                         1.0000      3328
   macro avg     1.0000    1.0000    1.0000      3328
weighted avg     1.0000    1.0000    1.0000      3328
````
****CLASSIFICATION REPORT - TEST DATA****
````
              precision    recall  f1-score   support

           0     0.7617    0.7645    0.7631       811
           1     0.7688    0.7660    0.7674       829

    accuracy                         0.7652      1640
   macro avg     0.7652    0.7652    0.7652      1640
weighted avg     0.7653    0.7652    0.7652      1640
````
****CONFUSION MATRIX AND ROC-AUC VISUALIZATION****

<br />
<p align = "left">
  <img src = "Images/Tree Reduced.png" width = 800>
</p>
<br />

Ok, we got better results, I would say excelent results. A 77% recall? Nice. But our Logisitc Regression still performed better. So... Im very sorry Decision Tree, but today is not you day :(

### Random Forest Original DF
Finally, lets evaluate our last model "Random Forest" starting with the original DataFrame:

****CLASSIFICATION REPORT - TRAINING DATA****
````
              precision    recall  f1-score   support

           0     0.9994    1.0000    0.9997      1673
           1     1.0000    0.9994    0.9997      1655

    accuracy                         0.9997      3328
   macro avg     0.9997    0.9997    0.9997      3328
weighted avg     0.9997    0.9997    0.9997      3328
````
****CLASSIFICATION REPORT - TEST DATA****
````
              precision    recall  f1-score   support

           0     0.8133    0.8113    0.8123       811
           1     0.8159    0.8179    0.8169       829

    accuracy                         0.8146      1640
   macro avg     0.8146    0.8146    0.8146      1640
weighted avg     0.8146    0.8146    0.8146      1640
````
****CONFUSION MATRIX AND ROC-AUC VISUALIZATION****

<br />
<p align = "left">
  <img src = "Images/Random Original.png" width = 800>
</p>
<br />

Clearly, League of Legends game results are more predictable than I thought. Its the third model that returns excelente results. We got a 81% recall which, althought its still under the Logistic Regression model, its still a consideraly high result.

### Random Forest Reduced DF
With the reduced DataFrame, Random Forest got the following results:

****CLASSIFICATION REPORT - TRAINING DATA****
````
              precision    recall  f1-score   support

           0     1.0000    1.0000    1.0000      1673
           1     1.0000    1.0000    1.0000      1655

    accuracy                         1.0000      3328
   macro avg     1.0000    1.0000    1.0000      3328
weighted avg     1.0000    1.0000    1.0000      3328
````
****CLASSIFICATION REPORT - TEST DATA****

````
              precision    recall  f1-score   support

           0     0.8002    0.8101    0.8051       811
           1     0.8120    0.8022    0.8070       829

    accuracy                         0.8061      1640
   macro avg     0.8061    0.8061    0.8061      1640
weighted avg     0.8062    0.8061    0.8061      1640
````
****CONFUSION MATRIX AND ROC-AUC VISUALIZATION****

<br />
<p align = "left">
  <img src = "Images/Random Reduced.png" width = 800>
</p>
<br />

Again some awesome results, an 80% recall, but is under the original DataFrame results and thus, below the Logistic Regression.

## Conclusion

After reviewing the data carefully, we can reach variuos conlclusions. In the first place, it is clear that a predictive model can be made with League of Legends because all 3 models got satisfactory recall results. Secondly, it seems that the original DataFrame serves best as training data rather the the reduced DataFrame, so `Sight_wards`, `Control_Wards` and `Plates` seem to be important even do they didnt have a high correlations with the wins. In addition, the Logistic Regression model seems to be the most apropiate algorithm for this data. This doesnt mean that therest are not good, Random Forest even got similiar results, but we were looking for the best of the best.

Finally, and probably the most important conclusion, is that we devolped a model capable of predicting with 82% accuracy. This means that only using information from the minute 14 of the game, the model predicts correctly the outcome of the game 82% of the times. Pretty nice, isn't it?

## Next Steps

As you may have noticed in the title, this is version 1 of this project, which means I would like to make a version 2. My idea for this second version would be, in fisrt place, to get a more extense and diverse data set, which would allow me to recofirm and adjust the results. Then, it would be good to test other algorithms, such as K-neighbors, Support Vector Machine, Naive Bayes, XGBoost and even Neural Networks.

Thank you very much for reading, I hope you enjoyed this project as much as I did. Bye :)
