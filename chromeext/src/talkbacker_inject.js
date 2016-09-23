(function () {
    'use strict';

    var injected_variables;
    var extensionSignalEvent;

    $(function () {
        injected_variables = JSON.parse(document.currentScript.getAttribute("data-variables"));
        initExtensionSignalMechanism();
        sendMessageToExtension({
            talkbacker: {
                active: is_article(),
            }
        });

        var d = $("<div/>");
        d.attr("id", "talkbacker_face")
            .html("<img src='http://megaicons.net/static/img/icons_sizes/315/1534/128/electric-shock-icon.png'/>")
            .css("position", "absolute")
            .css("top", 0)
            .css("right", 0)
            .css("display", "hidden")
        ;
        d.animate({
            "display":"block"
        }, 5000, function() {});

        d.click(function() {
            d.slideDown("slow", function() {
                suggestTalkback();
            });
        });

        d.appendTo($("body"));

        // suggestTalkback();
    });

    function suggestTalkback() {
        //alert(injected_variables['resource_hint']);
        console.log("TALKBACKER DEBUG:\n" +
            "resource hint: " + injected_variables['resource_hint'] + "\n" +
            "url: " + document.location.href
        );
        if (is_article()) {
            var article_id = get_article_id();
            console.log("ARTICLE!");
            // Do the big ass cross-site scripting
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "http://d3f28d1b.ngrok.io/talkbacks/" + article_id, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    // JSON.parse does not evaluate the attacker's scripts.
                    var resp = JSON.parse(xhr.responseText);
                    console.log("RESP: " + resp);
                    console.log("talkback: " + resp.talkback);
                    alert("Great article!\nWe recommend talking back with:\n\n" + resp.talkback);
                }
            };
            xhr.send();
        }
    }

    // ------------------------------------------------------------------------------------------------------

    function get_article_id() {
        return (document.location.href.split("/articles/")[1]);
    }

    function is_article() {
        return (get_article_id() !== undefined);
    }

    // ------------------------------------------------------------------------------------------------------

    function initExtensionSignalMechanism() {
        extensionSignalEvent = document.createEvent('Event');
        extensionSignalEvent.initEvent('__talkbacker_chrome_ext_event', true, true);
    }

    function sendMessageToExtension(data) {
        var hiddenDiv = document.getElementById('__talkbacker_chrome_ext_event_proxy');
        hiddenDiv.innerText = JSON.stringify(data);
        hiddenDiv.dispatchEvent(extensionSignalEvent);
    }

    // ------------------------------------------------------------------------------------------------------

    // sendMessageToExtension({
    //     labs_chrome_ext: {
    //         active: (enhancements.length > 0),
    //         enhancements: enhancements
    //     }
    // })
}());