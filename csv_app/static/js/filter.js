function applyFilter() {
    var table = document.getElementById('csv_table');
    var checkedColumns = document.querySelectorAll('input[name="columns"]:checked');
    var visibleColumns = [];
    var selectedColumn1 = document.getElementById('column_select1').value;
    var filterValue1 = document.getElementById('column_value1').value.toLowerCase();
    var selectedColumn2 = document.getElementById('column_select2').value;
    var filterValue2 = document.getElementById('column_value2').value.toLowerCase();
    var headerRow = table.rows[0];

    for (var i = 0; i < checkedColumns.length; i++) {
        visibleColumns.push(checkedColumns[i].value);
    }

    for (var j = 0; j < table.rows.length; j++) {
        var rowData = table.rows[j].innerText.toLowerCase();
        var displayRow = true;

        if (j === 0) {
            for (var k = 0; k < headerRow.cells.length; k++) {
                var columnName = headerRow.cells[k].innerText;
                if (!visibleColumns.includes(columnName)) {
                    headerRow.cells[k].style.display = 'none';
                } else {
                    headerRow.cells[k].style.display = 'table-cell';
                }
            }
            continue;
        }

        if (visibleColumns.length > 0) {
            for (var k = 0; k < table.rows[j].cells.length; k++) {
                var columnName = headerRow.cells[k].innerText;
                if (!visibleColumns.includes(columnName)) {
                    table.rows[j].cells[k].style.display = 'none';
                } else {
                    table.rows[j].cells[k].style.display = 'table-cell';
                }
            }
        }

        if (selectedColumn1 && filterValue1) {
            var columnIndex1 = Array.from(headerRow.cells).findIndex(cell => cell.innerText === selectedColumn1);
            var cellValue1 = table.rows[j].cells[columnIndex1].innerText.toLowerCase();
            displayRow = cellValue1.includes(filterValue1);
        }

        if (selectedColumn2 && filterValue2) {
            var columnIndex2 = Array.from(headerRow.cells).findIndex(cell => cell.innerText === selectedColumn2);
            var cellValue2 = table.rows[j].cells[columnIndex2].innerText.toLowerCase();
            displayRow = displayRow && cellValue2.includes(filterValue2);
        }

        if (displayRow) {
            table.rows[j].style.display = '';
        } else {
            table.rows[j].style.display = 'none';
        }
    }
}