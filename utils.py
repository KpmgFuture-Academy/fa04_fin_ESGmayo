import matplotlib.pyplot as plt

def plot_train_val_loss(train_loss, validation_loss):
    epochs = range(1, len(train_loss) + 1)
    plt.figure(figsize=(5, 4))
    plt.plot(epochs, train_loss, label='Train Loss', marker='o')
    plt.plot(epochs, validation_loss, label='Validation Loss', marker='x')
    
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training vs Validation Loss')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def make_result_df(target_, predict_):
    target_ = target_.reshape(-1)  # (N, 1) → (N,)
    predict_ = predict_.reshape(-1)
    return pd.DataFrame({
        'target': target_,
        'predict': predict_
    })

def plot_pred_target(result_df):
  plt.figure(figsize=(5, 4))
  plt.plot(result_df.index, result_df['target'], label='target', marker='o')
  plt.plot(result_df.index, result_df['predict'], label='predict', marker='x')
      
  plt.xlabel('Time')
  plt.ylabel('NOX')
  plt.title('Test Data')
  plt.legend()
  plt.grid(True)
  plt.tight_layout()
  plt.show()

def model_save(model, path):
  torch.save(model, path)

def model_load(path, pretraining= True, unfreeze_keys= None):
  model = torch.load(path, weights_only=False)
  
    if pretraining:
        for name, param in model.named_parameters():
            param.requires_grad = False

        if unfreeze_keys:
            for name, param in model.named_parameters():
                if any(key in name for key in unfreeze_keys):
                    param.requires_grad = True

    return model
