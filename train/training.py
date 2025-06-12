from tqdm import tqdm

def training(
        device,
        optimizer,
        loss_fn,
        num_epochs,
        model):
    total_training_loss = []
    total_validation_loss = []

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        for x, y in tqdm(train_loader, desc=f"[Epoch {epoch+1}]"):
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            preds = model(x) # 
            loss = loss_fn(preds, y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        train_loss /= len(train_loader)
        total_training_loss.append(train_loss)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                preds = model(x)
                loss = loss_fn(preds, y)
                val_loss += loss.item()

        val_loss /= len(val_loader)
        total_validation_loss.append(val_loss)

        print(f"[Epoch {epoch+1}] Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
    return total_training_loss, total_validation_loss
