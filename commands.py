import sublime_plugin
from SearchPanelEnhanced.search_panel import get_panel

class DisplaySearchPanelEnhanced(sublime_plugin.TextCommand):
  def run(self, edit, type = 'default', case_sensetive = True, backward = False):
    get_panel(self.view, type, case_sensetive, backward).show()

class GotoNextSearchPanelEnhancedResult(sublime_plugin.TextCommand):
  def run(self, edit, backward = False):
    panel = get_panel()

    if panel.panel == None or panel.panel.id() != self.view.id():
      panel.set_view(self.view)

    panel.next(backward)

class SearchPanelEnhancedComplete(sublime_plugin.TextCommand):
  def run(self, edit, select = False, end = False):
    panel = get_panel()
    panel.done(None, select, end, False)
    panel.close()

class SetSearchEnhancedOptions(sublime_plugin.TextCommand):
  def run(self, edit, type = None, case_sensetive = None, backward = False):
    panel = get_panel()
    panel.toggle_options(type, case_sensetive, backward)
    panel.change()

class SearchPanelEnhancedFindUnder(sublime_plugin.TextCommand):
  def run(self, edit, backward = False, next = False):
    if len(self.view.sel()) == 0:
      return

    panel = get_panel(self.view)
    if next:
      panel.next(backward)
    else:
      panel.set_options('default')
      word = self.view.sel()[0]
      if word.empty():
        word = self.view.word(word.b)

      panel.change(self.view.substr(word), backward)

class SearchPanelEnhancedSelectAll(sublime_plugin.TextCommand):
  def run(self, edit):
    panel = get_panel()
    panel.select_all()
    panel.close()

class SearchPanelEnhancedGotoHistory(sublime_plugin.TextCommand):
  def run(self, edit, backward = True):
    panel = get_panel()
    panel.goto_history(backward)

class SearchPanelEnhancedSelectToFound(sublime_plugin.TextCommand):
  def run(self, edit):
    panel = get_panel()
    panel.select_to_found()

class SearchPanelEnhancedDeleteToFound(sublime_plugin.TextCommand):
  def run(self, edit):
    panel = get_panel()
    panel.select_to_found()
    panel.get_view().run_command('delete_selection')