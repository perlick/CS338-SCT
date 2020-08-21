function toggleNav() {
	width = document.getElementById("sidenav").style.width;
	if(width=="250px"){
		document.getElementById("sidenav").style.width = '0px';
	}else{
		document.getElementById("sidenav").style.width = '250px';
	}
}

$(document).ready(function () {
	//Close nav when click ouside
	$(document).click(function () {
		var container = $("#sidenav");
		var button = $("#header i");
		if (!container.is(event.target) &&
			!container.has(event.target).length &&
			!button.is(event.target) &&
			!button.has(event.target).length) {
				container.width(0);
		}
	});
});