import sys
from pathlib import Path
root = str(Path(__file__).resolve().parents[1])
sys.path.append(root)
from src.prep_attr import *
from src.predict import *
from src.conf import *

def one_step_predict(attr_path = ATTR_PATH):
	write_attr()
	prdc = Predictor(attr_path, n = 1)
	prdc.train()
	pred, foo, foo2, foo3 = prdc.predict(evaluate = True)
	print(pred, foo, foo2, foo3)

def multi_step_predict():
	

if __name__ == '__main__':
	print(one_step_predict())