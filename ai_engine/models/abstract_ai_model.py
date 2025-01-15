import os
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import string
import random
import gc
import torch

#----------#

from utilities.singleton import Singleton

#======================================================================================================================#
# Abstract_AI_model
#======================================================================================================================#

class Abstract_AI_model(ABC, metaclass = Singleton):

    #------------------------------------------------------------------------------------------------------------------#

    def __init__(self, *args, **kwargs):
        # common inference parameters
        self._image_height = 1024.
        self._image_width = 1024.
        self._batch_size = 1
        # non inference parameters
        self._model_class_name = ''
        # device
        self._device = 'cuda'
        print('Model initialized: ', self._model_class_name)

    #------------------------------------------------------------------------------------------------------------------#

    @abstractmethod
    def _pre_processing(self, *args, **kwargs):
        pass

    #------------------------------------------------------------------------------------------------------------------#

    @abstractmethod
    def load_model(self, *args, **kwargs):
        pass

    #------------------------------------------------------------------------------------------------------------------#

    @abstractmethod
    def _inf(self, *args, **kwargs):
        pass

    #------------------------------------------------------------------------------------------------------------------#

    @abstractmethod
    def _post_processing(self, *args, **kwargs):
        pass

    #------------------------------------------------------------------------------------------------------------------#

    @abstractmethod
    def delete_model(self, *args, **kwargs):
        pass

    #------------------------------------------------------------------------------------------------------------------#

    # @abstractmethod
    # def transfer_model_to_cpu(self, *args, **kwargs):
    #     pass

    #------------------------------------------------------------------------------------------------------------------#

    # @abstractmethod
    # def transfer_model_to_cuda(self, *args, **kwargs):
    #     pass

    #------------------------------------------------------------------------------------------------------------------#

    def _get_save_path_for_media_without_extention(self):
        path = os.path.abspath('./medias/' + self._model_class_name + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))+ str(time.time()))
        print("Trying to save AI gen media at: ", path)
        return path
    

    #------------------------------------------------------------------------------------------------------------------#

    def clear_garbage(self):
        torch.cuda.empty_cache()
        gc.collect()

    #------------------------------------------------------------------------------------------------------------------#

    def process(self, *args, **kwargs):
        self._pre_processing(*args, **kwargs)
        self._inf(*args, **kwargs)
        output = self._post_processing(*args, **kwargs)
        self.clear_garbage()
        print('AI result: ', output)
        return output
    
    #------------------------------------------------------------------------------------------------------------------#

    def get_device(self):
        return self._device
    
#======================================================================================================================#
# End of Abstract_AI_model
#======================================================================================================================#