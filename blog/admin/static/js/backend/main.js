/**
* Bootstrap-Admin-Template by onokumus@gmail.com
* Version : 2.0.0 
* Author : Osman Nuri Okumuş 
* Copyright 2013
*/
$(function() {
    "use strict";

    $('a[href=#]').on('click', function(e){
      e.preventDefault();
    });
    
    
    $('a[data-toggle=tooltip]').tooltip();
    $('a[data-tooltip=tooltip]').tooltip();


    $('.minimize-box').on('click', function(e) {
        e.preventdefault();
        var $icon = $(this).children('i');
        if ($icon.hasclass('icon-chevron-down')) {
            $icon.removeclass('icon-chevron-down').addclass('icon-chevron-up');
        } else if ($icon.hasclass('icon-chevron-up')) {
            $icon.removeclass('icon-chevron-up').addclass('icon-chevron-down');
        }
    });
    
    $('.close-box').click(function() {
        $(this).closest('.box').hide('slow');
    });

    $('#changesidebarpos').on('click', function(e) {
        $('body').toggleclass('hide-sidebar');
    });
    
    $('li.accordion-group > a').on('click',function(e){
        $(this).children('span').children('i').toggleclass('icon-angle-down');
    });
});

function metisTable() {
    "use strict";

    /*----------- BEGIN datatable CODE -------------------------*/
    $('#dataTable').dataTable({
        "aaSorting": [[ 5, 'desc' ]],
        "sDom": "<'pull-right'l>t<'row'<'col-lg-6'f><'col-lg-6'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "Show _MENU_ entries"
        }
    });
    /*----------- END datatable CODE -------------------------*/

}