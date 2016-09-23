console.log('talkbacker: background script started');

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (typeof request === 'string') {
            try {
                request = JSON.parse(request);
            } catch (e) {
                return;
            }
        }
        if (request.talkbacker) {
            var version = getVersionString(version);

            if (request.talkbacker.active) {
                chrome.pageAction.show(sender.tab.id);
                chrome.pageAction.setTitle({
                    tabId: sender.tab.id,
                    title: "Click me to talk back on the article (Talkbacker v." + version + ")"
                });
            }
            else {
                // TODO: turn the icon off if we went from active page to inactive page
            }
        }
    }
);

function getVersionString() {
    if (isInstalledFromWebStore()) {
        return "v" + chrome.runtime.getManifest().version;
    }
    else if (isInstalledFromCRX()) {
        return "(CRX:" + chrome.runtime.getManifest().version + ")";
    }
    else {
        return "(LOCAL_DEV)";
    }
}

function isInstalledFromWebStore() {
    return (!!chrome.runtime.getManifest().update_url);
}

function isInstalledFromCRX() {
    // bah, this needs permissions which I don't care to request, just ignore
    return false;
    //// TODO: not sure this works, test it when someone installs via CRX
    //return (!isInstalledFromWebStore() && chrome.management.getSelf() && chrome.management.getSelf().installType == "normal");
}