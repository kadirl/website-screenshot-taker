// var elements = document.querySelectorAll('*');
// for (var i = 0; i < elements.length; i++) {
//     var element = elements[i];
//     var styles = window.getComputedStyle(element);

//     if (element.tagName == "HTML") continue;

//     // Calculate and apply the width and height based on the content
//     var boundingRect = element.getBoundingClientRect();
//     element.style.width = boundingRect.width + "px";
//     element.style.height = boundingRect.height + "px";
//     element.style.maxWidth = boundingRect.width + "px";
//     element.style.maxHeight = boundingRect.height + "px";
//     element.style.minWidth = boundingRect.width + "px";
//     element.style.minHeight = boundingRect.height + "px";

//     // Add additional CSS properties to replace as needed (e.g., padding, margin)
//     element.style.padding = styles.padding;
//     element.style.margin = styles.margin;

//     // Set box-sizing to border-box to maintain dimensions
//     element.style.boxSizing = 'border-box';

//     // Change everything except absolute to static
//     if (styles.position == 'fixed') {
//         // element.style.position = 'absolute';
//         element.remove()
//     } else if (styles.position == 'sticky') {
//         element.style.position = 'static';
//     }

// }

var elements = document.querySelectorAll('*');
for (var i = 0; i < elements.length; i++) {
    var element = elements[i];
    var styles = window.getComputedStyle(element);

    if (element.tagName == "HTML") continue;

    // Calculate and apply the width and height based on the content
    var boundingRect = element.getBoundingClientRect();
    element.style.width = boundingRect.width + "px";
    element.style.height = boundingRect.height + "px";
    element.style.maxWidth = boundingRect.width + "px";
    element.style.maxHeight = boundingRect.height + "px";
    element.style.minWidth = boundingRect.width + "px";
    element.style.minHeight = boundingRect.height + "px";

    // Add additional CSS properties to replace as needed (e.g., padding, margin)
    element.style.padding = styles.padding;
    element.style.margin = styles.margin;

    // Set box-sizing to border-box to maintain dimensions
    element.style.boxSizing = 'border-box';

    // Change everything except absolute to static
    if (styles.position == 'fixed'&& (element.innerHTML.includes('cookie') || element.innerHTML.includes('Cookie'))) {
        // element.style.position = 'absolute';
        element.style.setProperty('opacity', '0', 'important');
    } //else if (styles.position == 'sticky') {
        //element.style.position = 'static';
    //}

}