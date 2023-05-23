// Get all scroll event listeners attached to the window object
const scrollListeners = getEventListeners(window)['scroll'];
const wheelListeners = getEventListeners(window)['wheel']

// Remove all scroll event listeners
scrollListeners.forEach(listener => {
  window.removeEventListener('scroll', listener.listener);
});

// Remove all wheel event listeners
wheelListeners.forEach(listener => {
    window.removeEventListener('wheel', listener.listener);
  });