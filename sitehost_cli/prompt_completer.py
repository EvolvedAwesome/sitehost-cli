from sys import argv

# Prompt toolkit imports
from prompt_toolkit.document import Document
from prompt_toolkit.completion import Completer, CompleteEvent, Completion

# Typing
from typing import Iterable

class CLI_Completer(Completer):
    """Provides a completer class compatible with the prompt_toolkit
    that can do on the fly data-driven completion of terminal queries.
    """
    def __init__(self, module_list):
        super().__init__()
        self.module_list = module_list

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        text_so_far = document.current_line_before_cursor.split(" ")
        arg_index = len(text_so_far)-1
        word = document.get_word_before_cursor()

        if arg_index == 0:
            for command in self.module_list.keys():
                if word.strip() == "" or word.strip() in command:
                    yield Completion(command, start_position=-len(word))
            return

        if text_so_far[0].strip() in self.module_list.keys():
            python_method = self.module_list[text_so_far[0]]['command_py']
            # Check if this is a native method or a function. If
            # its a function without args_required then theres
            # no provided completions.
            # TODO: Implement name-based completions
            try:
                argument_list = python_method.args_required
            except AttributeError as e:
                return # Method is of type function

            # No completions if there are no arguments left
            if arg_index > len(argument_list):
                return

            for completion in argument_list[arg_index-1]._completions(dict(zip([arg.api_name for arg in argument_list], text_so_far[1:]))).items():
                if word.strip() == "" or any([word.strip() in compl for compl in list(completion)]):
                    yield Completion(completion[1], display=completion[0], start_position=-len(word)) 
            return