import uc480
import sys

class Testuc480:
	def setUp(self):
		self.camera = uc480.camera()

	def tearDown(self):
		self.camera.ExitCamera()

	def test_ReadEEPROM(self):
		self.camera.WriteEEPROM("test")
		content = self.camera.ReadEEPROM(count=len("test"))
		assert content == "test"

	def test_writeEEPROM(self):
		self.camera.WriteEEPROM("test")

	def test_AllocImageMem(self):
		assert self.camera.AllocImageMem() == 0


def test_init():
	camera = uc480.camera()
	camera.ExitCamera()