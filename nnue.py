import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
import numpy as np

from minimax import Minimax
from shiftagopy import Shiftago

class NNUE(Minimax):
	def __init__(self, game, depth=3):
		super().__init__(game, depth)

		self.input_size = self.size * self.size * 2 # board size * colors
		self.model = NNUEModel(input_size=self.input_size)

	def train(self, data, targets, epochs=10, lr=0.001, batch_size=32):
		optimizer = optim.Adam(self.model.parameters(), lr=lr)
		criterion = nn.MSELoss()

		dataset = torch.utils.data.TensorDataset(train_data, train_targets)
		dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

		for epoch in range(epochs):
			total_loss = 0.0
			for batch in dataloader:
				data, targets = batch
				optimizer.zero_grad()
				outputs = self.model(data)
				loss = criterion(outputs, targets)
				loss.backward()
				optimizer.step()
				total_loss += loss.item()
			
			print(f"Epoch [{epoch+1}/{epochs}], Loss: {total_loss/len(dataloader)}")
		return

	def evaluate(self, position_vector):
		self.model.eval()

		position_tensor = torch.tensor(position_vector, dtype=torch.float32).unsqueeze(0)
		with torch.no_grad():
			score = self.model(position_tensor).item()
		return score

	def test(self, test_data, test_targets):
		self.model.eval()
		
		with torch.no_grad():
			predictions = self.model(test_data)
			loss = nn.MSELoss()(predictions, test_targets)

		print(f"Test Loss: {loss.item()}")
		return loss.item()

	def load(self, filename="./model/nnue.torch"):
		self.model.load_state_dict(torch.load(filename))
		self.model.eval()  # Set to evaluation mode
		print(f"Model loaded from {filename}")
		return
	
	def export(self, filename="./model/nnue.torch"):
		torch.save(self.model.state_dict(), filename)
		print(f"Model saved as {filename}")
		return

class NNUEModel(nn.Module):
	def __init__(self, input_size, hidden_size=256, output_size=1):
		super(NNUEModel, self).__init__()

		# Create model architecture
		self.fc1 = nn.Linear(input_size, hidden_size)
		self.fc2 = nn.Linear(hidden_size, hidden_size)
		self.fc3 = nn.Linear(hidden_size, output_size)
		self.relu = nn.ReLU()

	def forward(self, x):
		x = self.relu(self.fc1(x))
		x = self.relu(self.fc2(x))
		x = self.fc3(x)
		return x
	
def load_training(filename="./data/positions.pt"):
	data, targets = torch.load(filename)
	return data, targets

if __name__ == "__main__":
	game = Shiftago()
	nnue = NNUE(game)

	# Load training data
	data, targets = load_training()
	train_data, test_data, train_targets, test_targets = train_test_split(data, targets, test_size=0.2)

	# Run training
	nnue.train(train_data, train_targets)
	nnue.test(test_data, test_targets)

	# Save model
	nnue.export()