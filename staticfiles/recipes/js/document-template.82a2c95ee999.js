$('#print').click(function()
{
	var prtContent = $('#document');
	var WinPrint = window.open('', '', 'left=0,top=0,width=800,height=900,toolbar=0,scrollbars=0,status=0');

	WinPrint.document.write(prtContent.html());
	WinPrint.document.close();
	WinPrint.focus();
	WinPrint.print();
});

$('#download').click(function()
{
	var title = $('h1.title').eq(0).text();
	var file = encodeURIComponent('\
		<meta charset="utf-8">' + $('#document').html()
	);

	$(this).attr('download', 'BakeToom - ' + title);
	$(this).attr('href', 'data:text/html;charset=utf-8,' + file);
});