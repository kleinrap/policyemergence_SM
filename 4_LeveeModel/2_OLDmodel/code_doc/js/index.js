$( document ).ready( function() {

collapsibleListGo('.collapsibleList');

// global var used to disable click event
var clickDisabled = 0;

function collapsibleListGo(elementSelector) {

	// search the dom for existance of .collapsibleList
	if ($(elementSelector).length > 0) {

		// iterate through all elementSelector li's
		$(elementSelector + ' li').each(function() {

			// test for children 
			if ($(this).children().length > 0) {
				// console.log('this has children');

				// add class closed
				$(this).addClass('collapsibleListClosed');

				// hide all children
				$(this).children().slideUp();

				$(this).click(function() {
					if (clickDisabled == 0) {

						$(this).toggleClass('collapsibleListClosed').toggleClass('collapsibleListOpen');
						$(this).children().slideToggle();

						// 100 ms delay to prevent parent item from closing
						resetClick(100);
					};
				});

			};
		});
	};
}; // end collapsibleListGo

function resetClick(timeoutTime) {
	clickDisabled = 1;

	var resetClickTimeout = setTimeout(function() {
		clickDisabled = 0;	
	}, timeoutTime);
}

});