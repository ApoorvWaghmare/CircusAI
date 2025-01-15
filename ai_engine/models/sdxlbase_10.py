from diffusers import DiffusionPipeline
import torch
import os
import gc

#----------#

from .abstract_ai_model import *

#======================================================================================================================#
# SDXLBase_10
#======================================================================================================================#

class SDXLBase_10(Abstract_AI_model):

    __base = None
    __refiner = None

    #------------------------------------------------------------------------------------------------------------------#

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model_class_name = self.__class__.__name__

    #------------------------------------------------------------------------------------------------------------------#

    def _pre_processing(self, *args, **kwargs):
        pass

    #------------------------------------------------------------------------------------------------------------------#

    def load_model(self, *args, **kwargs):    
        # load both base & refiner
        print(f'Loading {self._model_class_name} on {self._device}...')
        if self.__base == None:
            self.__base = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", 
                                                            torch_dtype = torch.float16, 
                                                            variant = "fp16", 
                                                            use_safetensors = True).to(self._device)
        if self.__refiner == None:
            self.__refiner = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0",
                                                            text_encoder_2 = self.__base.text_encoder_2,
                                                            vae = self.__base.vae,
                                                            torch_dtype = torch.float16,
                                                            use_safetensors = True,
                                                            variant = "fp16",).to(self._device)
        print(f'Loaded {self._model_class_name} on {self._device}')
            
    #------------------------------------------------------------------------------------------------------------------#

    # def transfer_model_to_cpu(self, *args, **kwargs):
    #     print(f'Current device {self._device}')
    #     if (self._device != 'cpu'):
    #         print(f'Loading {self._model_class_name} on cpu...')
    #         self.__base.to(torch.float32).to('cpu')
    #         self.__refiner.to(torch.float32).to('cpu')
    #         self._device = 'cpu'
    #         print(f'Loaded {self._model_class_name} on cpu')
    #     else:
    #         print(f'{self._model_class_name} already on cpu')

    #------------------------------------------------------------------------------------------------------------------#

    # def transfer_model_to_cuda(self, *args, **kwargs):
    #     print(f'Current device {self._device}')
    #     if (self._device != 'cuda'):
    #         print(f'Loading {self._model_class_name} on cuda...')
    #         self.__base.to(torch.float16).to('cuda')
    #         self.__refiner.to(torch.float16).to('cuda')
    #         self._device = 'cuda'
    #         self.clear_garbage()
    #         print(f'Loaded {self._model_class_name} on cuda')
    #     else:
    #         print(f'{self._model_class_name} already on cuda')

    #------------------------------------------------------------------------------------------------------------------#

    def _inf(self, prompt = None, *args, **kwargs):
        # run both experts
        image = self.__base(prompt = prompt,
                            num_inference_steps = 25,
                            denoising_end = 0.8,
                            output_type = "latent",).images
        image = self.__refiner(prompt = prompt,
                            num_inference_steps = 25,
                            denoising_start = 0.8,
                            image = image,).images[0]
        self.__image_path = self._get_save_path_for_media_without_extention() + '.png'
        image.save(self.__image_path)

    #------------------------------------------------------------------------------------------------------------------#

    def _post_processing(self, *args, **kwargs):
        if os.path.exists(self.__image_path):
            return self.__image_path
        else:
            return ''
        
    #------------------------------------------------------------------------------------------------------------------#
        
    def delete_model(self):
        print(f'Deleting {self._model_class_name}...')
        self.__base = None
        self.__refiner = None
        self.clear_garbage()
        print(f'Deleted {self._model_class_name}')

#======================================================================================================================#
# End of SDXLBase_10
#======================================================================================================================#