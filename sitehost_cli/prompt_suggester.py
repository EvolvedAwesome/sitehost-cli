from typing import Optional

from prompt_toolkit.document import Document
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

class CLI_Suggester(AutoSuggest):
    """Provides a prompt toolkit compatable suggester class that simply uses
    the defined names of arguments to provide suggestions about what the user should
    input.
    """
    def __init__(self, module_list):
        super().__init__()
        self.module_list = module_list

    def get_suggestion(self, buffer, document: Document) -> Optional[Suggestion]:
        text_so_far = document.current_line_before_cursor.split(" ")
        arg_index = len(text_so_far)-1
        word = document.get_word_before_cursor()

        if arg_index == 0:
            return None
        
        if text_so_far[0].strip() in self.module_list.keys():
            python_method = self.module_list[text_so_far[0]]['command_py']
            try:
                argument_list = python_method.args_required
            except AttributeError as e:
                # Its a function, not a CLI arugment class
                # We will try to extract an argument list from the docstring
                usage_line = [line for line in python_method.__doc__.split("\n") if "Usage:" in line]
                if not usage_line:
                    return 
                argument_list = usage_line[0].split("Usage:")[-1].strip().split(" ")[1:]
        else:
            return
            
        if arg_index > len(argument_list):
            return

        if len(word.strip()) > 0:
            return None

        try:
            return Suggestion(argument_list[arg_index-1].name)
        except AttributeError:
            return Suggestion(str(argument_list[arg_index-1]))