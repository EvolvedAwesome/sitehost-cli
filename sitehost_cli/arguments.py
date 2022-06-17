from dataclasses import dataclass
from typing import Callable 
from jsonpath_ng import parse
import copy

# Package imports
from sitehost_cli.module import CLI_Module
from sitehost_cli.exceptions import *

@dataclass
class CLI_Argument:
    module: CLI_Module
    name: str
    api_name: str

    def _completions(self, args_dict = None):
        return {}

    @property
    def _default_value(self):
        """When the argument is set to simply "#", then a default
        argument will be pulled from this property
        """
        raise NotEnoughArgumentsException(f"No value for {self.name} was provided.")
    
    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name

    def get_filter_copy(self):
        filter_c = copy.copy(self)
        filter_c.api_name = f"filters[{self.api_name}]"
        return filter_c

    def get_params_copy(self):
        filter_c = copy.copy(self)
        filter_c.api_name = f"params[{self.api_name}]"
        return filter_c
    
    def get_single_list_copy(self):
        filter_c = copy.copy(self)
        filter_c.api_name = f"{self.api_name}s[0]"
        return filter_c
    
    def get_api_name_copy(self, api_name: str):
        filter_c = copy.copy(self)
        filter_c.api_name = api_name 
        return filter_c


@dataclass
class Smart_CLI_Argument(CLI_Argument):
    list_api_endpoint: str
    api_path: str
    label_path: str = None
    dynamic_completion: bool = False
    context_attributes: list = None 

    def __post_init__(self):
        self.api_path_regex = parse(self.api_path)
        self.__completions = None

        if self.label_path is not None:
            self.label_path_regex = parse(self.label_path)
            self.__label_completions = None
        
        self.completion_dict = None 

    def _completions(self, args_dict = None):
        """Returns an array of the potential completions for a CLI
        argument.
        """
        context_message = {}

        # We always include client_id
        try:
            client_id = args_dict['client_id'] 
            context_message['client_id'] = client_id
        except KeyError as e:
            client_id = self.module.client_id

        # Generalised context
        if self.context_attributes is not None:
            for ca, filter_bool in self.context_attributes:
                try:
                    data = args_dict[ca]
                except KeyError as e:
                    data = None
                if filter_bool:
                    context_message[f"filters[{ca}]"] = data
                else:
                    context_message[ca] = data

        if client_id is None:
            client_id = self.module.client_id

        if self.completion_dict is None or client_id != self.module.client_id or self.dynamic_completion: 
                response = self.module._post_request(self.list_api_endpoint, context_message).json()
                response = response['return']
                self.__completions = [match.value.strip() for match in self.api_path_regex.find(response) if match.value.strip() != ""]

                if self.label_path is not None:
                    self.__label_completions = [match.value.strip() if match.value.strip() != "" else self.__completions[index] for index, match in enumerate(self.label_path_regex.find(response))]
                    self.completion_dict = dict(zip(self.__label_completions, self.__completions))
                else:
                    self.completion_dict = dict(zip(self.__completions, self.__completions))

        return self.completion_dict 

@dataclass
class Generic_CLI_Argument(CLI_Argument):
    completions: list 
    default_value: str = None 
    completions_labels: list = None

    @property
    def _default_value(self):
        """When the argument is set to simply "#", then a default
        argument will be pulled from this property
        """
        if self.default_value is not None:
            return self.default_value
        else:
            if len(self.completions) > 0:
                return self.completions[0]
            else:
                raise NotEnoughArgumentsException(f"No value for {self.name} was provided.")

    def _completions(self, args_dict = None):
        """Returns an array of the potential completions for a CLI
        argument.

        TODO: Add a context manager based on the document input
        """
        if self.completions_labels is not None:
            return dict(zip(self.completions_labels, self.completions))
        else:
            return dict(zip(self.completions, self.completions))

@dataclass
class Client_ID_Arugment(CLI_Argument):

    def _completions(self, args_dict = None):
        if self.module.client_id is not None:
            return {self.module.client_id:self.module.client_id}
        else:
            return {} 
            
    @property
    def _default_value(self):
        if self.module.client_id is not None:
            return self.module.client_id
        else:
            print("No client id is set!")
            raise NotEnoughArgumentsException(f"No client id is set!")