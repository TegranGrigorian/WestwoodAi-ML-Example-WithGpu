'''
This program will just test the cuda with a torch function
'''

#imports
import torch

if not torch.cuda.is_available():
    print("Cuda not avaliable please follow install drivers and verify you chose the right torch package!")
else:
    print(f"CUDA is available. Device count: {torch.cuda.device_count()}")
