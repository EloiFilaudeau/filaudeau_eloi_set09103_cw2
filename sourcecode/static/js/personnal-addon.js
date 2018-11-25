// soundplayer function
var music = document.getElementById('player');
var btn = document.getElementById('btn-player');
function playAudio() {
    if (music.paused) {
        music.play();
        // remove play, add pause
        btn.className = "";
        btn.className = "fa fa-pause";
    } else {
        music.pause();
        // remove pause, add play
        btn.className = "";
        btn.className = "fa fa-play";
    }
}

$(document).ready(function() {
    // clickable row for bootstrap table
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

    // search bar
    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    // mark stars
    $("tr").each(function() {
        if ($(this).find("td:eq(8)").text()=="1") {
            $(this).find("td:eq(8)").replaceWith("<i style='padding-top:15px;' class='fa fa-star'></i>");
        } else if ($(this).find("td:eq(8)").text()=="0") {
            $(this).find("td:eq(8)").replaceWith("");
        }
    });

     // button filter
     $('.filterable .btn-filter').click(function(){
         var $panel = $(this).parents('.filterable'),
         $filters = $panel.find('.filters input'),
         $tbody = $panel.find('.table tbody');
         if ($filters.prop('disabled') == true) {
             $filters.prop('disabled', false);
             $filters.first().focus();
             $('th').css("font-size","0px");
         } else {
             $filters.val('').prop('disabled', true);
             $tbody.find('.no-result').remove();
             $tbody.find('tr').show();
             $('th').css("font-size","17px");
         }
     });

     // filter form
     $('.filterable .filters input').keyup(function(e){
         /* Ignore tab key */
         var code = e.keyCode || e.which;
         if (code == '9') return;
         /* Useful DOM data and selectors */
         var $input = $(this),
         inputContent = $input.val().toLowerCase(),
         $panel = $input.parents('.filterable'),
         column = $panel.find('.filters th').index($input.parents('th')),
         $table = $panel.find('.table'),
         $rows = $table.find('tbody tr');
         /* Dirtiest filter function ever ;) */
         var $filteredRows = $rows.filter(function(){
             var value = $(this).find('td').eq(column).text().toLowerCase();
             return value.indexOf(inputContent) === -1;
         });
         /* Clean previous no-result if exist */
         $table.find('tbody .no-result').remove();
         /* Show all rows, hide filtered ones (never do that outside of a demo ! xD) */
         $rows.show();
         $filteredRows.hide();
         /* Prepend no-result row if all rows are filtered */
         if ($filteredRows.length === $rows.length) {
             $table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="'+ $table.find('.filters th').length +'">No result found</td></tr>'));
         }
     });

 });
