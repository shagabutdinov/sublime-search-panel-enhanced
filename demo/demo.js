/* Redmine - project management software
   Copyright (C) 2006-2014  Jean-Philippe Lang */

function collapseAllRowGroups(el) {
  var tbody = $(el).parents('tbody').first();

  // 1. set cursor to start of tbody and add variable
  tbody.children('tr').each(function(index) {
    if ($(this).hasClass('group')) {
      $(this).removeClass('open');
    } else {
      $(this).hide();
    }
  });
}

// 2. rename function
function expandAllRowGroups(el) {
  var tbody = $(el).parents('tbody').first();
  tbody.children('tr').each(function(index) {
    if ($(this).hasClass('group')) {
      $(this).addClass('open');
    } else {
      $(this).show();
    }
  });
}

function toggleAllRowGroups(el) {
  // 3. Select all for refactoring
  var tr = $(el).parents('tr').first();
  if (tr.hasClass('open')) {
    collapseAllRowGroups(el);
  } else {
    expandAllRowGroups(el);
  }
}