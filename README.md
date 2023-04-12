# Prediction of Handle Time of a Contact by an Agent in Webex Contact Center
Given an agent is assigned a contact, we want to pRedict how long it will take to handle the contact using metadata about an on-going interaction such as agent, skills, date and time, queue in which the call has landed, priority of contact, customer id, agent details etc.

## About The Data
From our systems we obtained data in various formats & after various relevant aggregations & filters we dumped it into csv. This is the starting point of consumption of this data. 
The columns are:
 1.   id                         145303 non-null  object
 2.  matchedSkills              145303 non-null  object -> subset of all the skills required for this contact among all the skills this agent has 
 3.   lastTeam                   145303 non-null  object -> the team to which the agent belongs
 4.   requiredSkills             145303 non-null  object -> skill requirements from the contact
 5.  createdTime                145303 non-null  int64  -> time when the contact entered the system
 6.   endedTime                  145303 non-null  int64  -> wrap up time of the contact(we will get rid of this in the subsequent data processing)
 7.   origin                     145303 non-null  object -> customer's identifier(phone number, email-id, chat id)
 8.   destination                145303 non-null  object -> toll free route point destination where the customer connects
 9.   contactReason              30692 non-null   object -> only relevant in chat, denotes the reason for the cotnact
 10.   channelSubType             145303 non-null  object -> finer distinction among telephony, chat & email
 11.  channelType                145303 non-null  object -> telephony, chat & email
 12.  holdCount                  145303 non-null  int64  -> number of times customer was put on hold
 13.  holdDuration               145303 non-null  int64  -> how long the hold episodes lasted
 14.  selfserviceCount           145303 non-null  int64  -> how many times customer encountered self service(IVR)
 15.  selfserviceDuration        145303 non-null  int64  -> how long the self-service episodes lasted
 16.  connectedCount             145303 non-null  int64  -> how many times this customer connected to an agent, can be multiple if he/she hopped among queues. 
 17.  connectedDuration          145303 non-null  int64  -> our prediction variable. How long customer and agent were connected.
 18.  ringingDuration            145303 non-null  int64  -> how long it took to connect to system
 19.  queueDuration              145303 non-null  int64  -> how long was customer waiting in queue
 20.  queueCount                 145303 non-null  int64  -> how many times customer was queued
 21.  routingType                144790 non-null  object -> internal algorithm of the contact center
 22.  isHandledByPreferredAgent  145303 non-null  bool   -> one particular feature of the contact center where customers can choose their agent 
 23.  lastQueue                  145303 non-null  object -> queue from which this agent picked up this contact
 24.  contributors               145303 non-null  object -> agent
 25.  skillDiff                  145303 non-null  float64 -> difference in skill b/w agent & contact's requirement
 26.  queue                      145303 non-null  object -> queue(engineered column)
 27.  agent                      145302 non-null  object -> agent(engineered column)
 28.  team                       145303 non-null  object -> team(engineered column)
 29.  rs                         20081 non-null   object -> required skill(engineered column)
 30.  ms                         20081 non-null   object -> matched skills(engineered column)

This data is for a particular organisation using this contact center. Each row represents an interaction between an agent and a customer(contact). This contact center supports 3 media channels - telephony, chat & email.

NOTE: in the constants file you will notice two names frequently appearing - lion king and maersk. These are two orgs for which we got data initially. Finally we got proper data only for lion king and all our modelling are based on that.

## How to Execute the project
The project is designed to consume data from data.csv & go through various steps. Each of the steps are executed in a file. Following are the details:
1. `1_imputation.py` - consumes data.csv, does imputation, drops unneccesary columns, remove outliers, train test split & outputs `imputed_data_train.csv & imputed_data_test.csv`
2. `2_feature_engineering.py` - consumes `imputed_data_<test/train>.csv`, breaks created timestamp to year, month, week, day etc & outputs `engineered_data_train.csv & engineered_data_test.csv`
3. `3_encoding.py` - consumes `engineered_data_<test/train>.csv`, perform encoding for categorical columns and output `encoded_data_train.csv & encoded_data_test.csv`
4. `4_eda.py` - performs various EDA
5. `\model` folder contains a file for each model such linear regression, bagging, boosting, decision tree, random forest etc. In these there are two flavours, train on default parameters, or do training with hyper parameter tuning & come up with best parameters.
6. `all_model.py` - is a master file for training & evaluation of each model. One can do hyper parameter tuning here as well, or use the parameters found in the individual files. Finally we can also do split modelling based on the channel type of contact, because a email's connected duration will typically be very different from a telephony contact's connected duration.

Hence starting with data.csv we can progressively run each step of imputation, feature engineering, encoding, eda & finally modelling to get the results. Each step produces an output which is consumed by the next step and so on.

## Authors
Biswarup Das Sarma(biswarup.cst@gmail.com)