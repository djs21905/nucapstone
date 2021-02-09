import matplotlib.pyplot as plt
import os
import numpy as np

def plot_performance(model_history,name,folder):
    losses = model_history['loss']
    accs = model_history['accuracy']
    val_losses = model_history['val_loss']
    val_accs = model_history['val_accuracy']
    epochs = len(model_history)
    plt.figure(figsize=(12, 4))
    for i, metrics in enumerate(zip([losses, accs], [val_losses, val_accs], ['Loss', 'Accuracy'])):
        plt.subplot(1, 2, i + 1)
        plt.plot(range(epochs), metrics[0], label='Training {}'.format(metrics[2]))
        plt.plot(range(epochs), metrics[1], label='Validation {}'.format(metrics[2]))
        plt.xticks(np.arange(0,epochs,1.0))
        plt.title('Training and Validation '+ metrics[2] + " for " + name)
        plt.legend()
    fn = os.path.join(folder,name+"_Acc_Loss.png")
    plt.savefig(fn)
    plt.show()