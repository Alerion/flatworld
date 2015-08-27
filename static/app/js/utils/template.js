import $ from 'jquery';
import React from 'react';


// Shortcut for rendering JSX
export default function jsx(jsx) {
    return $(React.renderToStaticMarkup(jsx));
}