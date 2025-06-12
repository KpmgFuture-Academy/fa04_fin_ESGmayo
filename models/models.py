import torch
import torch.nn as nn
import numpy as np

class OperationTimeEncoder(nn.Module):
    def __init__(self, in_ch):  # in_ch = 24
        super().__init__()
        h = int(np.sqrt(in_ch))
        self.conv1d = nn.Sequential(
            nn.Conv1d(in_ch, h, kernel_size=3, padding=1),
            nn.GELU(),
            nn.Conv1d(h, h, kernel_size=3, padding=1),
            nn.GELU(),
        )
        self.out_dim = h

    def forward(self, x):
        # x: [B, 24, T] → [B, h, T] → mean(T) → [B, h]
        return self.conv1d(x).mean(dim=2)

class TimeSeries(nn.Module):
    def __init__(self, in_ch, out_ch, hidden_size, multi_encoding=True):
        super().__init__()
        self.multi_encoding = multi_encoding

        if multi_encoding:
            self.time_encoder = OperationTimeEncoder(in_ch=24)
            self.lstm = nn.LSTM(
                input_size=in_ch - 24,
                hidden_size=hidden_size // 2,
                num_layers=2,
                dropout=0.2,
                batch_first=True,
                bidirectional=True
            )
            self.conv = nn.Sequential(
                nn.Conv1d(in_ch - 24, hidden_size, kernel_size=3, padding=1),
                nn.GELU(),
                nn.Conv1d(hidden_size, hidden_size, kernel_size=3, padding=1),
                nn.GELU(),
            )
            self.out = nn.Sequential(
                nn.Linear(hidden_size * 2 + self.time_encoder.out_dim, hidden_size),
                nn.GELU(),
                nn.Linear(hidden_size, out_ch),
                nn.ReLU()
            )
        else:
            self.lstm = nn.LSTM(
                input_size=in_ch,
                hidden_size=hidden_size // 2,
                num_layers=2,
                dropout=0.2,
                batch_first=True,
                bidirectional=True
            )
            self.conv = nn.Sequential(
                nn.Conv1d(in_ch, hidden_size, kernel_size=3, padding=1),
                nn.GELU(),
                nn.Conv1d(hidden_size, hidden_size, kernel_size=3, padding=1),
                nn.GELU(),
            )
            self.out = nn.Sequential(
                nn.Linear(hidden_size * 2, hidden_size),
                nn.GELU(),
                nn.Linear(hidden_size, out_ch),
                nn.ReLU()
            )

    def forward(self, x):
        if self.multi_encoding:
            x_feat = x[:, :, :-24]
            x_time = x[:, :, -24:]
            lstm_out, _ = self.lstm(x_feat)
            lstm_out = lstm_out[:, -1, :]
            conv_out = self.conv(x_feat.permute(0, 2, 1)).mean(dim=2)
            time_out = self.time_encoder(x_time.permute(0, 2, 1))
            x = torch.cat([lstm_out, conv_out, time_out], dim=1)
        else:
            lstm_out, _ = self.lstm(x)
            lstm_out = lstm_out[:, -1, :]
            conv_out = self.conv(x.permute(0, 2, 1)).mean(dim=2)
            x = torch.cat([lstm_out, conv_out], dim=1)
        return self.out(x)
