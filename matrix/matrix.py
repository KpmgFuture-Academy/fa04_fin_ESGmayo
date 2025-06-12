import numpy as np

def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

def rmse(y_true, y_pred):
  return np.sqrt(np.mean((y_pred - y_true) ** 2))

def AL1_loss(y_true, y_pred, a=5.0, b=2.0):
    E = y_pred - y_true

    under_loss = np.zeros_like(E)
    over_loss = np.zeros_like(E)

    # Underprediction: E <= 0
    under_mask_1 = (E <= 0) & (E > -1)
    under_mask_2 = (E <= -1)
    under_loss[under_mask_1] = a * np.abs(E[under_mask_1])
    under_loss[under_mask_2] = a * (E[under_mask_2] ** 2)

    # Overprediction: E > 0
    over_mask_1 = (E > 0) & (E < 1)
    over_mask_2 = (E >= 1)
    over_loss[over_mask_1] = b * (E[over_mask_1] ** 2)
    over_loss[over_mask_2] = b * np.abs(E[over_mask_2])

    total_loss = np.mean(under_loss + over_loss)
    return total_loss
