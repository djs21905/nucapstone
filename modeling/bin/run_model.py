import tensorflow as tf
from tensorflow import keras
import pandas as pd
import datetime
from bin.html_functions import ez_display as d

def run_model(model,model_name,x,y,epochs=10,batch_size=128,validation_split=0.15, verbose = 1):
    model_history = {}
    model_history['name'] = model_name
    x_train = x['train']
    x_test = x['test']
    y_train = y['train']
    y_test = y['test']
    start = datetime.datetime.now()
    if verbose == 1:
        d(f'<h3>Running {model_name}</h3>')
        d(f'<h4>Training</h4>')
    history = model.fit(x_train,
                        y_train,
                        epochs = epochs,
                        batch_size = batch_size,
                        validation_split = validation_split,
                        verbose = verbose)
    duration = datetime.datetime.now() - start
    if verbose == 1:
        print("Total Train Time: {}".format(duration))
        d(f'<h4>Testing</h4>')
    model_history['duration'] = duration
    model_history['history'] = pd.DataFrame(history.history)
    model_loss, model_acc = model.evaluate(x_test,y_test)
    model_history['test_accuracy'] = model_acc
    model_history['loss'] = model_loss
    if verbose == 1:
        print('test set accuracy: ', model_acc * 100)
    return model, model_history