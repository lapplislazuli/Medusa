# Utilites to computed GuidedBackprop SaliencyMasks
from aux_functions.saliency import SaliencyMask

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
    import tensorflow as tf
except ImportError:
    import warnings
    note = ("\n\n\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n" +
            "# WARNING: Anaconda Module 'tensorflow' is not installed yet                        #\n" +
            "# TO ENSURE EXECUTABILITY, PLEASE RUN Section 'Managing Anaconda Environment' first #\n" +
            "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n\n")
    warnings.warn(note)
    
try:
    import keras.backend as K
    from keras.models import load_model
except ImportError:
    import warnings
    note = ("\n\n\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n" +
            "# WARNING: Anaconda Module 'keras' is not installed yet                             #\n" +
            "# TO ENSURE EXECUTABILITY, PLEASE RUN Section 'Managing Anaconda Environment' first #\n" +
            "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n\n")
    warnings.warn(note) 
    

    
class GuidedBackprop(SaliencyMask):
    # A SaliencyMask class that computes saliency masks with GuidedBackProp.
    # This implementation copies the TensorFlow graph to a new graph with the ReLU
    # gradient overwritten as in the paper:
    # https://arxiv.org/abs/1412.6806
    
    GuidedReluRegistered = False

    def __init__(self, model, output_index=0, custom_loss=None):
        # Constructs a GuidedBackprop SaliencyMask.

        if GuidedBackprop.GuidedReluRegistered is False:
            @tf.RegisterGradient("GuidedRelu")
            def _GuidedReluGrad(op, grad):
                gate_g = tf.cast(grad > 0, "float32")
                gate_y = tf.cast(op.outputs[0] > 0, "float32")
                return gate_y * gate_g * grad
        GuidedBackprop.GuidedReluRegistered = True
        
        # Create a dummy session to set the learning phase to 0 (test mode in keras) without
        # inteferring with the session in the original keras model. This is a workaround
        # for the problem that tf.gradients returns error with keras models that contains
        # Dropout or BatchNormalization.
        # Basic Idea: save keras model => create new keras model with learning phase set to 0 => save
        # the tensorflow graph => create new tensorflow graph with ReLU replaced by GuiededReLU.
        
        model.save('/tmp/gb_keras.h5') 
        with tf.Graph().as_default(): 
            with tf.Session().as_default(): 
                K.set_learning_phase(0)
                load_model('/tmp/gb_keras.h5', custom_objects={"custom_loss":custom_loss})
                session = K.get_session()
                tf.train.export_meta_graph()
                
                saver = tf.train.Saver()
                saver.save(session, '/tmp/guided_backprop_ckpt')

        self.guided_graph = tf.Graph()
        with self.guided_graph.as_default():
            self.guided_sess = tf.Session(graph = self.guided_graph)

            with self.guided_graph.gradient_override_map({'Relu': 'GuidedRelu'}):
                saver = tf.train.import_meta_graph('/tmp/guided_backprop_ckpt.meta')
                saver.restore(self.guided_sess, '/tmp/guided_backprop_ckpt')

                self.imported_y = self.guided_graph.get_tensor_by_name(model.output.name)[0][output_index]
                self.imported_x = self.guided_graph.get_tensor_by_name(model.input.name)

                self.guided_grads_node = tf.gradients(self.imported_y, self.imported_x)
        
    def get_mask(self, input_image):
        # Returns a GuidedBackprop mask.
        x_value = np.expand_dims(input_image, axis=0)
        guided_feed_dict = {}
        guided_feed_dict[self.imported_x] = x_value        

        gradients = self.guided_sess.run(self.guided_grads_node, feed_dict = guided_feed_dict)[0][0]

        return gradients
