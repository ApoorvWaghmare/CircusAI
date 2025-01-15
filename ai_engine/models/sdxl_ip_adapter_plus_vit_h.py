from diffusers import AutoPipelineForText2Image
from diffusers.utils import load_image
import torch
import os
from transformers import CLIPVisionModelWithProjection
import gc

#----------#

from .abstract_ai_model import *

#======================================================================================================================#
# SDXL_ip_adapter_plus_vit_h
#======================================================================================================================#

class SDXL_ip_adapter_plus_vit_h(Abstract_AI_model):

    __image_encoder = None
    __pipeline = None
    __generator = None

    #------------------------------------------------------------------------------------------------------------------#

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model_class_name = self.__class__.__name__

    #------------------------------------------------------------------------------------------------------------------#

    def _pre_processing(self, prompted_media_ref = None, *args, **kwargs):
        self.__ip_adapter_image = load_image(prompted_media_ref)

    #------------------------------------------------------------------------------------------------------------------#

    def load_model(self, *args, **kwargs):    
        print(f'Loading {self._model_class_name} on {self._device}...')
        if self.__image_encoder == None:
            self.__image_encoder = CLIPVisionModelWithProjection.from_pretrained("h94/IP-Adapter",
                                                                                subfolder = "models/image_encoder",
                                                                                torch_dtype = torch.float16)
        if self.__pipeline == None:
            self.__pipeline = AutoPipelineForText2Image.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                                                        image_encoder = self.__image_encoder,
                                                                        torch_dtype = torch.float16).to(self._device)
            self.__pipeline.load_ip_adapter("h94/IP-Adapter", 
                                            subfolder="sdxl_models", 
                                            weight_name = "ip-adapter-plus_sdxl_vit-h.safetensors")
            self.__pipeline.set_ip_adapter_scale(0.3)
        if self.__generator == None:
            self.__generator = torch.Generator(device = self._device).manual_seed(0)
        print(f'Loaded {self._model_class_name} on {self._device}')

    #------------------------------------------------------------------------------------------------------------------#

    # def transfer_model_to_cpu(self, *args, **kwargs):
    #     print(f'Current device {self._device}')
    #     if (self._device != 'cpu'):
    #         print(f'Loading {self._model_class_name} on cpu...')
    #         self.__pipeline.to(torch.float32).to('cpu')
    #         self.__generator = torch.Generator(device = 'cpu').manual_seed(0)
    #         self._device = 'cpu'
    #         print(f'Loaded {self._model_class_name} on cpu')
    #     else:
    #         print(f'{self._model_class_name} already on cpu')

    #------------------------------------------------------------------------------------------------------------------#

    # def transfer_model_to_cuda(self, *args, **kwargs):
    #     print(f'Current device {self._device}')
    #     if (self._device != 'cuda'):
    #         print(f'Loading {self._model_class_name} on cuda...')
    #         self.__pipeline.to(torch.float16).to('cuda')  
    #         self.__generator = torch.Generator(device = 'cuda').manual_seed(0)
    #         self._device = 'cuda'
    #         self.clear_garbage()
    #         print(f'Loaded {self._model_class_name} on cuda')
    #     else:
    #         print(f'{self._model_class_name} already on cuda')
        
    #------------------------------------------------------------------------------------------------------------------#

    def _inf(self, positive_prompt = None, negative_prompt = None, *args, **kwargs):
        image = self.__pipeline(prompt = positive_prompt,
                                ip_adapter_image = self.__ip_adapter_image,
                                negative_prompt = negative_prompt,
                                num_inference_steps = 25,
                                generator = self.__generator,).images[0]
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
        self.__image_encoder = None
        self.__pipeline = None
        self.__generator = None
        self.clear_garbage()
        print(f'Deleted {self._model_class_name}')

#======================================================================================================================#
# End of SDXL_ip_adapter_plus_vit_h
#======================================================================================================================#