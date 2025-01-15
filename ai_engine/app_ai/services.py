# import multiprocessing
# import threading

#----------#

from utilities.singleton import Singleton
from models.sdxlbase_10 import SDXLBase_10
from models.sdxl_ip_adapter_plus_vit_h import SDXL_ip_adapter_plus_vit_h
from app_watermark.services import WatermarkService

#======================================================================================================================#
# MemoryManagementService
#======================================================================================================================#

# class MemoryManagementService(metaclass = Singleton):

#     def __init__(self):
#         self.model_dict = {}
#         self.initialize_models()
#         self.__sdxl_process = None
#         self.__ip_process = None

#     def initialize_models(self):
#         try:
#             self.model_dict['SDXL_ip_adapter_plus_vit_h'] = SDXL_ip_adapter_plus_vit_h()
#             self.model_dict['SDXLBase_10'] = SDXLBase_10()
#             # process1 = multiprocessing.Process(target=self.model_dict['SDXL_ip_adapter_plus_vit_h'].load_model, args=('cuda',))
#             # process1.start()
#             # process2 = multiprocessing.Process(target=self.model_dict['SDXLBase_10'].load_model, args=('cpu',))
#             # process2.start()
#             # process1.join()
#             # process2.join()
#             self.model_dict['SDXL_ip_adapter_plus_vit_h'].load_model('cuda')
#             self.model_dict['SDXLBase_10'].load_model('cpu')
#         except Exception as e:
#             print(e)

#     def __SDXLBase_10_to_cpu(self):
#         self.model_dict['SDXLBase_10'].load_model('cpu')
#         self.model_dict['SDXLBase_10'].clear_garbage()

#     def __SDXL_ip_adapter_plus_vit_h_to_cpu(self):
#         self.model_dict['SDXL_ip_adapter_plus_vit_h'].load_model('cpu')
#         self.model_dict['SDXL_ip_adapter_plus_vit_h'].clear_garbage()

#     def get_SDXLBase_10(self):
#         if self.model_dict['SDXL_ip_adapter_plus_vit_h'].get_device() == 'cuda':
#             self.model_dict['SDXL_ip_adapter_plus_vit_h'].delete_model()
#         if self.model_dict['SDXLBase_10'].get_device() != 'cuda':
#             # if self.__sdxl_process != None:
#             #     self.__sdxl_process.join()
#             self.model_dict['SDXLBase_10'].transfer_model_to_cuda()
#         if self.model_dict['SDXL_ip_adapter_plus_vit_h'].get_device() != 'cpu':
#             self.__ip_process = multiprocessing.Process(target = self.__SDXL_ip_adapter_plus_vit_h_to_cpu)
#             self.__ip_process.start()
#         return self.model_dict['SDXLBase_10']

#     def get_SDXL_ip_adapter_plus_vit_h(self):
#         if self.model_dict['SDXLBase_10'].get_device() == 'cuda':
#             self.model_dict['SDXLBase_10'].delete_model()
#         if self.model_dict['SDXL_ip_adapter_plus_vit_h'].get_device() != 'cuda':
#             # if self.__ip_process != None:
#             #     self.__ip_process.join()
#             self.model_dict['SDXL_ip_adapter_plus_vit_h'].transfer_model_to_cuda()
#         if self.model_dict['SDXLBase_10'].get_device() != 'cpu':
#             self.__sdxl_process = multiprocessing.Process(target=self.__SDXLBase_10_to_cpu)
#             self.__sdxl_process.start()
#         return self.model_dict['SDXL_ip_adapter_plus_vit_h']

#======================================================================================================================#
# End of MemoryManagementService
#======================================================================================================================#

#======================================================================================================================#
# StartUpService
#======================================================================================================================#

class StartUpService:

    @staticmethod
    def initialize_model_management_service():
        try:
            SDXLBase_10()
            SDXL_ip_adapter_plus_vit_h()
        except Exception as e:
            print(e)
        
#======================================================================================================================#
# End of StartUpService
#======================================================================================================================#

#======================================================================================================================#
# Text2ImageService
#======================================================================================================================#
    
class Text2ImageService:

    @staticmethod
    def process(prompt: str) -> str:
        try:
            SDXL_ip_adapter_plus_vit_h().delete_model()
            SDXLBase_10().load_model()
            image_path = SDXLBase_10().process(prompt = prompt)
            return WatermarkService.add_watermark(image_path = image_path)
        except Exception as e:
            print(e)
            return ''

#======================================================================================================================#
# End of Text2ImageService
#======================================================================================================================#

#======================================================================================================================#
# TextImage2ImageService
#======================================================================================================================#

class TextImage2ImageService:

    @staticmethod
    def process(prompted_media_ref: str, prompt: str) -> str:
        try:
            SDXLBase_10().delete_model()
            SDXL_ip_adapter_plus_vit_h().load_model()
            prompted_media_ref = WatermarkService.remove_watermark(image_path = prompted_media_ref)
            image_path = SDXL_ip_adapter_plus_vit_h().process(prompted_media_ref = prompted_media_ref,
                                                              positive_prompt = prompt,
                                                              negative_prompt = None)
            return WatermarkService.add_watermark(image_path=image_path)
        except Exception as e:
            print(e)
            return ''

#======================================================================================================================#
# End of TextImage2ImageService
#======================================================================================================================#
