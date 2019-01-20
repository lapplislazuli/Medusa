# Utilities to compute SaliencyMasks.
try:
    import numpy as np 
except ImportError:
    import warnings
    note = ("\n\n\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n" +
            "# WARNING: Anaconda Module 'numpy' is not installed yet                           #\n" +
            "# TO ENSURE EXECUTABILITY, PLEASE RUN Section 'Managing Anaconda Environment' first #\n" +
            "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n\n")
    warnings.warn(note)

try:
    import keras.backend as K
except ImportError:
    import warnings
    note = ("\n\n\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n" +
            "# WARNING: Anaconda Module 'keras' is not installed yet                             #\n" +
            "# TO ENSURE EXECUTABILITY, PLEASE RUN Section 'Managing Anaconda Environment' first #\n" +
            "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n\n")
    warnings.warn(note)     
    


class SaliencyMask(object):
    # Base class for saliency masks. Alone, this class doesn't do anything.
    def __init__(self, model, output_index=0):
        # Constructs a SaliencyMask.
        # Args:
        #    model: the keras model used to make prediction
        #    output_index: the index of the node in the last layer to take derivative on
        
        pass

    def get_mask(self, input_image):
        # Returns an unsmoothed mask.
        # Args:
        #    input_image: input image with shape (H, W, 3).
        
        pass

    def get_smoothed_mask(self, input_image, stdev_spread=.2, nsamples=50):
        # Returns a mask that is smoothed with the SmoothGrad method.
        # Args:
        #    input_image: input image with shape (H, W, 3).
        
        stdev = stdev_spread * (np.max(input_image) - np.min(input_image))

        total_gradients = np.zeros_like(input_image)
        for i in range(nsamples):
            noise = np.random.normal(0, stdev, input_image.shape)
            x_value_plus_noise = input_image + noise

            total_gradients += self.get_mask(x_value_plus_noise)

        return total_gradients / nsamples

class GradientSaliency(SaliencyMask):
    # A SaliencyMask class that computes saliency masks with a gradient.

    def __init__(self, model, output_index=0):
        # Define the function to compute the gradient
        input_tensors = [model.input,        # placeholder for input image tensor
                         K.learning_phase(), # placeholder for mode (train or test) tense
                        ]
        # gradients = model.optimizer.get_gradients(model.output[0][output_index], model.input)
        gradients = K.gradients(model.output[0][output_index], model.input)
        self.compute_gradients = K.function(inputs=input_tensors, outputs=gradients)

    def get_mask(self, input_image):
        # Returns a vanilla gradient mask.
        # Args:
        #    input_image: input image with shape (H, W, 3).
                
        # Execute the function to compute the gradient
        x_value = np.expand_dims(input_image, axis=0)
        gradients = self.compute_gradients([x_value, 0])[0][0]

        return gradients
