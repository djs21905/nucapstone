import matplotlib.pyplot as plt
import os
import numpy as np

def plot_performance(df,name,folder):
    losses = df['loss']
    accs = df['accuracy']
    val_losses = df['val_loss']
    val_accs = df['val_accuracy']
    epochs = len(df)
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