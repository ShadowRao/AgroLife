def main():
    # importing the required libraries

    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split

    # Reading the csv file
    data = pd.read_csv("C:/xampp/htdocs/nitte/crop/cpdata.csv")
    # print(data.head(1))

    # Creating dummy variable for target i.e label
    label = pd.get_dummies(data.label).iloc[:, 1:]
    data = pd.concat([data, label], axis=1)
    data.drop("label", axis=1, inplace=True)
    # print('The data present in one row of the dataset is')
    # print(data.head(1))
    train = data.iloc[:, 0:4].values
    test = data.iloc[:, 4:].values

    # Dividing the data into training and test set
    X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=0.3)

    from sklearn.preprocessing import StandardScaler

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Importing Decision Tree classifier
    from sklearn.tree import DecisionTreeRegressor

    clf = DecisionTreeRegressor()

    # Fitting the classifier into training set
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)

    from sklearn.metrics import accuracy_score

    # Finding the accuracy of the model
    a = accuracy_score(y_test, pred)
    acc = "The accuracy of this model is: " + str(a * 100)

    # Using firebase to import data to be tested
    from firebase import firebase

    firebase = firebase.FirebaseApplication("https://cropit-eb156.firebaseio.com/")
    tp = firebase.get("/Realtime", None)
    ah = tp["Air Humidity"]
    atemp = tp["Air Temp"]
    shum = tp["Soil Humidity"]
    pH = tp["Soil pH"]
    rain = tp["Rainfall"]

    l = []
    l.append(ah)
    l.append(atemp)
    l.append(pH)
    l.append(rain)
    predictcrop = [l]

    crops = [
        "wheat",
        "mungbean",
        "Tea",
        "millet",
        "maize",
        "lentil",
        "jute",
        "cofee",
        "cotton",
        "ground nut",
        "peas",
        "rubber",
        "sugarcane",
        "tobacco",
        "kidney beans",
        "moth beans",
        "coconut",
        "blackgram",
        "adzuki beans",
        "pigeon peas",
        "chick peas",
        "banana",
        "grapes",
        "apple",
        "mango",
        "muskmelon",
        "orange",
        "papaya",
        "watermelon",
        "pomegranate",
    ]
    cr = "rice"
    # crops = ['lentil','moth beans','coconut','blackgram','adzuki beans','pigeon peas','chick peas','banana','grapes','apple','mango','muskmelon','orange','papaya','watermelon','pomegranate']
    # Predicting the crop
    predictions = clf.predict(predictcrop)
    count = 0
    l = []
    # print(predictions)
    i = 0
    while i < 30:
        if predictions[0][i] == 1:

            c = crops[i]
            l.append(c)
            count = count + 1
            # print(count)
            crops.remove(crops[i])
            # print(crops)
            predictions = clf.predict(predictcrop)
            if count >= 4:
                break
        i = i + 1
        if i == 29:
            i = 0

    # print(l)

    # Sending the predicted crop to database
    cp = firebase.put("/croppredicted", "crop", c)
    s=''
    for i in l:
        s+=i +' '
    s += str(a * 100)
    print(s)


main()
