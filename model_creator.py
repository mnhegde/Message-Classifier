import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pickle
from messages import getMsgData

def open_batch_data(filename):
    with open (filename, 'rb') as fp:
        batch_data = pickle.load(fp)
        return(batch_data)

def overwrite_model_file():
    with open('color_model.pkl', 'wb') as output:  # Overwrites any existing file.
        pickle.dump(message_classifier_model, output, pickle.HIGHEST_PROTOCOL)
        print("file overwrited")

data = getMsgData()

x_train = data[0] #the features
y_train = data[1] #the classifiers

batch_size = len(y_train)

#model creation
message_classifier_model = MLPClassifier(alpha=0.01, 
                                        batch_size=batch_size, 
                                        epsilon=1e-08, 
                                        hidden_layer_sizes=(300,), 
                                        learning_rate='adaptive', 
                                        max_iter=50000)

#model training
message_classifier_model.fit(x_train,y_train)

#model testing
x_pred = message_classifier_model.predict(x_train)
accuracy=accuracy_score(y_true=y_train, y_pred=x_pred)
print("Accuracy: {:.2f}%".format(accuracy*100))