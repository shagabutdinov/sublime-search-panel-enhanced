import sublime
import sublime_plugin
import re

try:
  from StatusMessage import status_message
except ImportError as error:
  sublime.error_message("Dependency import failed; please read readme for " +
   "StatusMessage plugin for installation instructions; to disable this " +
   "message remove this plugin; message: " + str(error))
  raise error

panel = None
def get_panel(view = None, type = None, case_sensetive = None, backward = None):
  global panel
  if panel == None:
    panel = SearchPanel()

  if view != None:
    panel.set_view(view)

  panel.set_options(type, case_sensetive, backward, False)
  return panel

class SearchPanel():
  def __init__(self):
    self.value = None
    self.expression = None

    self.type = 'default'
    self.case_sensetive = False
    self.backward = False

    self.panel = None
    self.initial = None
    self.view = None

    self.history = []
    self.history_index = None

  def set_view(self, view):
    self.view = view
    self._set_cursors()

  def get_view(self):
    return self.view

  def show(self):
    self.prevent_cancel = False

    self._set_cursors()

    initial = ''
    if len(self.view.sel()) == 1 and not self.view.sel()[0].empty():
      initial = self.view.substr(self.view.sel()[0])
    elif self.value != None:
      initial = self.value

    # change are fired before assignment; panel should be visible at this point
    self.panel = True
    self.panel = sublime.active_window().show_input_panel('', initial,
      self.done, self.change, self._cancel)

    self.panel.run_command('select_all')
    self.history_index = len(self.history) - 1

  def _set_cursors(self):
    self.cursors = []
    for sel in self.view.sel():
      self.cursors.append(sublime.Region(sel.b, sel.b))

    self.initial = self.cursors.copy()

  def toggle_options(self, type = None, case_sensetive = None, backward = None):
    if type != None:
      if self.type == type:
        self.type = 'default'
      else:
        self.type = type

    if case_sensetive != None:
      if case_sensetive == "toggle":
        self.case_sensetive = not self.case_sensetive
      else:
        self.case_sensetive = case_sensetive

    if backward != None:
      self.backward = backward

    self._set_status('')

  def set_options(self, type = None, case_sensetive = None, backward = None,
    set_status = True):

    if type != None:
      self.type = type

    if case_sensetive != None:
      self.case_sensetive = case_sensetive

    if backward != None:
      self.backward = backward

    if set_status:
      self._set_status('')

  def _get_status_icon(self):
    message = '🔎'
    if self.type == 'regexp':
      message += '✱'
    elif self.type == 'word':
      message += 'W'
    elif self.type == 'fuzzy':
      message += 'F'

    if not self.case_sensetive:
      message += 'C'

    return message

  def _set_status(self, text):
    if self.view == None:
      return

    message = self._get_status_icon() + ' ' + text
    status_message.set(self.view, 'search_panel_enhanced', message)

  def next(self, backward = False):
    if self.expression == None:
      self.view.erase_regions('search_panel_enhanced')
      return None

    if self.backward:
      backward = not backward

    found, highlights = self._search(self.expression, backward)
    if found != None:
      cursors = []
      for index, entry in enumerate(found):
        if entry != None:
          cursors.append(entry)
        else:
          cursors.append(self.cursors[index])
      self.cursors = cursors

    self._next_highlight_found(highlights, found)
    self._next_set_status(highlights)

  def _next_highlight_found(self, highlights, found):
    self.view.add_regions('search_panel_enhanced', highlights, '?', '',
      sublime.DRAW_NO_FILL | sublime.DRAW_EMPTY)

    if self.panel == None:
      self._set_selection()
    else:
      self.view.add_regions('search_panel_enhanced_found', found, 'string', '')
      self.view.show(found[0])

  def _next_set_status(self, highlights):
    value = str(self.value)
    if len(str(value)) > 30:
      value = value[:10] + '...' +value[: -10]

    message = value + ' '
    message += '(' +str(len(highlights)) + ')'

    self._set_status(message)

  def get_panel(self):
    return self.panel

  def change(self, value = None, backward = False):
    self.cursors = self.initial

    if value == None:
      value = self.value or ''

    self.expression, self.value = self._get_expression(value)
    if self.panel == True:
      return

    self.next(backward)

  def _search(self, expression, backward):
    shift, matches, wrapped = self._get_matches(expression, backward)
    if len(matches) == 0:
      return self.cursors, self.cursors

    if wrapped and len(self.cursors) == 1:
      match = matches[0]
      result = [sublime.Region(match.start(1) + shift, match.end(1) + shift)]
      found_indexes = [0]
    else:
      found_indexes, result = self._find_new_cursors(backward, shift, matches)

    highlights = []
    for index, match in enumerate(matches):
      if index in found_indexes:
        continue

      region = sublime.Region(match.start(1) + shift, match.end(1) + shift)
      highlights.append(region)

    return result, highlights

  def _find_new_cursors(self, backward, shift, matches):
    found_indexes, result = [], []
    for cursor in self.cursors:
      found = False
      for index, match in enumerate(matches):
        match_start, match_end = match.start(1) + shift, match.end(1) + shift

        found = ((
          backward and
          cursor.a > match_start
        ) or (
          not backward and
          cursor.a < match_start
        ))
          # previous_match == None

        if found:
          result.append(sublime.Region(match_start, match_end))
          found_indexes.append(index)
          break

      if not found:
        result.append(cursor)

    return found_indexes, result

  def _get_matches(self, expression, backward):
    text, shift = self._get_text(backward)

    matches = list(re.finditer(expression, text))
    if backward == None:
      return shift, matches, None

    wrapped = False
    if len(matches) == 0:
      wrapped = True
      text, shift = self._get_text(backward, True)
      matches = list(re.finditer(expression, text))

    if backward:
      matches = list(reversed(matches))

    return shift, matches, wrapped

  def _get_text(self, backward, wrapped = False):
    if wrapped and backward != None:
      backward = not backward

    if backward == None:
      region = sublime.Region(0, self.view.size())
    elif backward:
      region = sublime.Region(0, self.cursors[-1].a - 1)
    else:
      region = sublime.Region(self.cursors[0].b + 1, self.view.size())

    text = self.view.substr(region)
    return text, region.a

  def _get_expression(self, value):
    if len(value) < 2:
      result = None
    elif self.type == 'default':
      result = r'(' + re.escape(value) + r'\w*)'
    elif self.type == 'word':
      result = r'\W(' + re.escape(value) + r')\W'
    elif self.type == 'regexp':
      result = r'(' + value + ')'
    elif self.type == 'fuzzy':
      result = ''
      for char in value:
        result += re.escape(char) + r'\w*'
      result = '(' +result + ')'
    else:
      raise Exception('Unknown search type: ' +self.type)

    if result != None:
      try:
        if self.case_sensetive:
          result = re.compile(result)
        else:
          result = re.compile(result, re.IGNORECASE)
      except re.error as error:
        result = None
        self._set_status('{0}'.format(error))

    return result, value

  def done(self, _, select = False, end = False, bug_workaround = True):
    self._append_to_history()

    self.panel = None
    self._erase_regions()
    self._set_selection(select, end, bug_workaround)

  def _append_to_history(self, text = None):
    if text == None:
      text = self.panel.substr(sublime.Region(0, self.panel.size()))

    if len(self.history) > 0 and text == self.history[-1]:
      return

    self.history.append(text)
    self.history_index = len(self.history) - 1

  def goto_history(self, backward = True):
    text = None
    if backward:
      self.history_index -= 1
      if self.history_index < 0:
        self.history_index = 0
    else:
      self.history_index += 1
      if self.history_index > len(self.history) - 1:
        self.history_index = len(self.history) - 1
        text = ''

    self.panel.run_command('select_all')
    self.panel.run_command('left_delete')

    if len(self.history) == 0:
      return

    if text == None:
      text = self.history[self.history_index]

    self.panel.run_command('insert', {'characters': text})

  def _cancel(self):
    self._append_to_history()
    self.panel = None

    if self.prevent_cancel:
      return

    self.cursors = self.initial
    self._set_selection()
    self._erase_regions()

  def _set_selection(self, select = False, end = False, bug_workaround = True):
    self.view.sel().clear()
    for cursor in self.cursors:
      start, finish = cursor.a, cursor.a
      if select:
        finish = cursor.b
      elif end:
        start, finish = cursor.b, cursor.b

      self.view.sel().add(sublime.Region(start, finish))

    self.view.show(self.view.sel()[0].a)

    # invisible selection sublime bug workaround
    if bug_workaround:
      self.view.run_command('move', {"by": "characters", "forward": False})
      self.view.run_command('move', {"by": "characters", "forward": True})

  def close(self):
    self.prevent_cancel = True
    sublime.active_window().run_command('hide_panel', {'cancel': False})
    self._erase_regions()

  def select_all(self):
    if self.expression == None:
      self._erase_regions()
      return None

    regions = []
    _, matches, _ = self._get_matches(self.expression, None)
    for match in matches:
      regions.append(sublime.Region(match.start(1), match.end(1)))

    self.view.sel().clear()
    self.view.sel().add_all(regions)
    self.close()

  def select_to_found(self):
    if self.expression == None:
      self._erase_regions()
      return None

    regions = []
    for index, initial in enumerate(self.initial):
      target = self.cursors[index].a
      if target < initial.a:
        target = self.cursors[index].b

      regions.append(sublime.Region(initial.a, target))

    self.view.sel().clear()
    self.view.sel().add_all(regions)
    self.close()

  def _erase_regions(self):
    self.view.erase_regions('search_panel_enhanced')
    self.view.erase_regions('search_panel_enhanced_found')