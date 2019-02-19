from Imports import *

def createModel():
    #creates our model
    #each add fucntion adds a layer to our machine learning model.
    #creates a sequential model
    with open('objs.pkl','rb') as f:  
        networkInput, pitchNames, numNotes, nVocab , normalNetworkInput = pickle.load(f)

    model = Sequential()
    #adds LSTM layer with 256 nodes and a shape matching our normalised input
    model.add(LSTM(256,input_shape=(normalNetworkInput.shape[1], normalNetworkInput.shape[2]),return_sequences=True))
    #drop out randomly sets a draction rate of input units to 0 during training time with helps to prevent overfitting.
    model.add(Dropout(0.3))
    #adds another lstm layer with 512 nodes.
    model.add(LSTM(512, return_sequences=True))
    #dropout layer
    model.add(Dropout(0.3))
    #256 nodes lstm
    model.add(LSTM(256))
    #adds a standard densely connected NN layer with 256 nodes dense meaning each node recives input from all of the nodes in the previous layer.
    model.add(Dense(256))
    #dropout layer
    model.add(Dropout(0.3))
    #final dense layer with nVocab number of nodes so that we have 1 node per possible note value.
    model.add(Dense(nVocab))
    #adds a softmax activation to the previous dense layer.
    model.add(Activation('softmax'))
    #compiles out created model using the categorical_crossentropy loss function and the rmsprop optimiser.
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')#creates out model
    #each add fucntion adds a layer to our machine learning model.
    #creates a sequential model
    model = Sequential()
    #adds LSTM layer with 256 nodes and a shame matching our normalised input
    model.add(LSTM(256,input_shape=(normalNetworkInput.shape[1], normalNetworkInput.shape[2]),return_sequences=True))
    #drop out randomly sets a draction rate of input units to 0 during training time with helps to prevent overfitting.
    model.add(Dropout(0.3))
    #adds another lstm layer with 512 nodes.
    model.add(LSTM(512, return_sequences=True))
    #dropout layer
    model.add(Dropout(0.3))
    #256 nodes lstm
    model.add(LSTM(256))
    #adds a standard densely connected NN layer with 256 nodes dense meaning each node recives input from all of the nodes in the previous layer.
    model.add(Dense(256))
    #dropout layer
    model.add(Dropout(0.3))
    #final dense layer with nVocab number of nodes so that we have 1 node per possible note value.
    model.add(Dense(nVocab))
    #adds a softmax activation to the previous dense layer.
    model.add(Activation('softmax'))
    #compiles out created model using the categorical_crossentropy loss function and the rmsprop optimiser.
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    return model