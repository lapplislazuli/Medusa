# Utilities to compute an IntegratedGradients SaliencyMask.
from aux_functions.saliency import GradientSaliency

try:
    import numpy as np 
except ImportError:
    import warnings
    note = ("\n\n\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n" +
            "# WARNING: Anaconda Module 'numpy' is not installed yet                             #\n" +
            "# TO ENSURE EXECUTABILITY, PLEASE RUN Section 'Managing Anaconda Environment' first #\n" +
            "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n\n")
    warnings.warn(note)

    
    
class IntegratedGradients(GradientSaliency):
    # A SaliencyMask class that implements the integrated gradients method.
    # https://arxiv.org/abs/1703.01365
    
    def GetMask(self, input_image, input_baseline=None, nsamples=100):
        # Returns a integrated gradients mask.
        if input_baseline == None:
            input_baseline = np.zeros_like(input_image)

        assert input_baseline.shape == input_image.shape

        input_diff = input_image - input_baseline

        total_gradients = np.zeros_like(input_image)

        for alpha in np.linspace(0, 1, nsamples):
            input_step = input_baseline + alpha * input_diff
            total_gradients += super(IntegratedGradients, self).get_mast(input_step)

        return total_gradients * input_diff
