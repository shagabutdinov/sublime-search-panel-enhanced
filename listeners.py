import sublime_plugin
import sublime

from SearchPanelEnhanced import search_panel

try:
  from StatusMessage import status_message
except ImportError:
  sublime.error_message("Dependency import failed; please read readme for " +
   "StatusMessage plugin for installation instructions; to disable this " +
   "message remove this plugin")



class ContextResponder(sublime_plugin.EventListener):
  def on_query_context(self, view, key, operator, operand, _):
    if key != 'is_search_panel_enhanced_visible':
      return None

    visible = search_panel.get_panel().get_panel() != None

    if operator == sublime.OP_EQUAL:
      return visible == operand
    elif operator == sublime.OP_NOT_EQUAL:
      return visible != operand

    raise Exception('Unsupported operator: ' + str(operator))


class HighlightsCleaner(sublime_plugin.EventListener):
  def on_selection_modified_async(self, view):
    panel = search_panel.get_panel()
    if panel.get_panel() != None or panel.view == None:
      return

    last_command, _, _ = panel.view.command_history(0)
    is_reset_required = (
      last_command != 'goto_next_search_panel_enhanced_result' and
      last_command != 'search_panel_enhanced_find_under'
    )

    if not is_reset_required:
      return

    panel.view.erase_regions('search_panel_enhanced')
    status_message.erase(view, 'search_panel_enhanced')