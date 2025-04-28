#this script will test of the cuda is available or not, if not it will raise an error
import torch
def test_cuda_availability():
    if not torch.cuda.is_available():
        raise EnvironmentError("CUDA is not available. Please check your CUDA installation.")
    else:
        print("CUDA is available.")