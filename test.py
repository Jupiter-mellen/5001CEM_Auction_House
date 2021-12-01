import random 
import os



path = os.path.dirname(os.path.abspath(__file__))
print("hello")

print(path)
print(os.path.dirname(os.path.join(path+"\\static\\images\\")))