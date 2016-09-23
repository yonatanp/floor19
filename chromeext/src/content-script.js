function inject() {
    addEventProxyElement('__talkbacker_chrome_ext_event_proxy', '__talkbacker_chrome_ext_event');

    addScript(local("sweetalert.min.js"));
    addStyle(local("sweetalert.css"));

    var main_script = addScript(local('talkbacker_inject.js'), '__talkbackerInjectScript', {
        // example for passing extension resource hints
        messagebox_image: local("images/talkbacker-64.png"),
    });
}

// ----------------------------------------------------------------------------------------------------------

function local(rel_path) {
    return chrome.extension.getURL(rel_path);
}

function addScript(url, id, variables) {
    var html = document.getElementsByTagName('html')[0];
    var script = window.document.createElement('script');
    script.src = url;
    if (id !== undefined) {
        script.id = id;
    }
    if (variables !== undefined) {
        script.setAttribute("data-variables", JSON.stringify(variables));
    }
    html.appendChild(script);
    return script;
}

function addStyle(url, id) {
    var html = document.getElementsByTagName('html')[0];
    var style = window.document.createElement("link");
    style.type = "text/css";
    style.rel = "stylesheet";
    style.href = url;
    if (id !== undefined) {
        style.id = id;
    }
    html.appendChild(style);
    return style;
}

function addEventProxyElement(id, listenter_event_name) {
    var html = document.getElementsByTagName('html')[0];
    var eventProxyElement = document.createElement('div');
    eventProxyElement.id = id;
    eventProxyElement.style.display = 'none';

    eventProxyElement.addEventListener(listenter_event_name, function () {
        var eventData = eventProxyElement.innerText;
        chrome.runtime.sendMessage(eventData);
    });

    html.appendChild(eventProxyElement);
}

// ----------------------------------------------------------------------------------------------------------

// function injectAccordingToPageVisited() {
//     var angularFound = !!(document.querySelector('.ng-binding, ' +
//         '[ng-app], [data-ng-app], ' +
//         '[ng-controller], [data-ng-controller], ' +
//         '[ng-repeat], [data-ng-repeat]') ||
//     document.querySelector('script[src*="angular.js"], ' +
//         'script[src*="angular.min.js"]'));
//
//     if (angularFound) {
//         inject();
//     }
// }

// ----------------------------------------------------------------------------------------------------------

// injectAccordingToPageVisited();
inject()
