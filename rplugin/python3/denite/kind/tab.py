import typing

from itertools import filterfalse
from denite.kind.openable import Kind as Openable
from denite.util import Nvim, UserContext, Candidate

class Kind(Openable):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)
        self.name = 'tab'
        self.default_action = 'open'

    def action_open(self, context: UserContext) -> None:
        for target in context['targets']:
            self.vim.command(f'tabnext {target["action__tab_number"]}')
