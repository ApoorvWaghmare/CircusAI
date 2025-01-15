import logging
from functools import wraps
from types import FunctionType, MethodType
from typing import Union, Callable, Tuple, Any
from django.db import transaction, DEFAULT_DB_ALIAS

#----------#

from .error import ExecutionError

#----------#

logger = logging.getLogger(__name__)

#======================================================================================================================#
# Service
#======================================================================================================================#

class Service:

    @classmethod
    def wrap(cls, service_class: object) -> object:
        service_type = getattr(service_class, 'service_type', None)

        for key in dir(service_class):
            value = getattr(service_class, key)

            if isinstance(value, FunctionType) or isinstance(value, MethodType):
                wrapped_method = None

                if service_type == 'Query':
                    wrapped_method = cls.query(value)

                elif service_type == 'Atomic':
                    wrapped_method = cls.atomic(value)
                
                else:
                    raise ExecutionError("service_type Must Be Either 'Query' or 'Atomic'")

                setattr(service_class, key, wrapped_method)

        return service_class
    
    #------------------------------------------------------------------------------------------------------------------#
    
    @staticmethod
    def query(method: Union[FunctionType, MethodType]) -> Callable:        
        
        @wraps(method)
        def wrapper(*args, **kwargs) -> Tuple[Any, bool]:
            result = None

            try:
                result = method(*args, **kwargs)
                    
            except Exception as error:
                logger.error(f'Query in {method.__name__}')
                logger.error(error)

            else:
                logger.info(f'Query in {method.__name__}')
            
            finally:
                return result

        return wrapper
    
    #------------------------------------------------------------------------------------------------------------------#

    @staticmethod
    def atomic(method: Union[FunctionType, MethodType]) -> Callable:        
        
        @wraps(method)
        def wrapper(*args, **kwargs) -> Tuple[Any, bool]:
            is_error = False

            try:
                with transaction.atomic(using = DEFAULT_DB_ALIAS):
                    method(*args, **kwargs)
                    
            except Exception as error:
                logger.error(f'Transaction in {method.__name__}')
                logger.error(error)
                is_error = True
            
            else:
                logger.info(f'Transaction in {method.__name__}')

            finally:
                return is_error

        return wrapper
    
#======================================================================================================================#
# End of Service
#======================================================================================================================#