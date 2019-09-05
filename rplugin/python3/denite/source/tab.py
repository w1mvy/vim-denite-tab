import typing

from os.path import getatime, exists
from time import localtime, strftime, time
from sys import maxsize

from denite.base.source import Base
from denite.util import Nvim, UserContext, Candidates
from pynvim.api import Tabpage

class Source(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)
        self.name = 'tab'
        self.kind = 'tab'
        self.vars = {
            'date_format': '%d %b %Y %H:%M:%S'
        }

    def on_init(self, context: UserContext) -> None:
        context['__alter_tab_number'] = self.vim.current.tabpage


    def gather_candidates(self, context: UserContext) -> Candidates:
        rjust = len(f'{len(self.vim.tabpages)}') + 1
        ljustnm = 0
        rjustft = 0
        tabattrs = []
        for tabattr in [self._get_attributes(context, tab)
                for tab in self.vim.tabpages]:
            if tabattr['name'] == '':
                tabattr['file_name'] = 'No Name'
                tabattr['path'] = ''
            else:
                tabattr['file_name'] = self.vim.call('fnamemodify', tabattr['name'], ':~:.')
                tabattr['path'] = self.vim.call('fnamemodify', tabattr['name'], ':p')
            ljustnm = max(ljustnm, len(tabattr['file_name']))
            rjustft = max(rjustft, len(tabattr['filetype']))
            tabattrs.append(tabattr)
            candidates = [self._convert(x, rjust, ljustnm, rjustft)
                for x in tabattrs]
        return candidates

    def _convert(self, tab_attr: typing.Dict[str, typing.Any],
             rjust: int, ljustnm: int, rjustft: int) -> typing.Dict[
                 str, typing.Any]:
        return {
            'tab_number': tab_attr['number'],
            'word': tab_attr['file_name'],
            'abbr': '{} {} {}'.format(
                str(tab_attr['number']).rjust(rjust, ' '),
                tab_attr['file_name'].ljust(ljustnm, ' '),
                (f' [{tab_attr["filetype"]}]'
                 if tab_attr['filetype'] != '' else '').rjust(rjustft+3)
            ),
            'action__tab_number': tab_attr['number']
        }

    def _get_attributes(self, context: UserContext, tab: Tabpage) -> typing.Dict[str, typing.Any]:
        attr = {
            'number' : tab.number,
            'name' : tab.window.buffer.name
        }
        attr.update({
            'filetype': self.vim.call('getbufvar', tab.window.buffer.number, '&filetype')
        })
        return attr
