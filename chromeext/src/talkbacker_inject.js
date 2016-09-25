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
            .css("position", "fixed")
            .css("top", 0)
            .css("right", 0)
            .css("padding", "15px 15px 0 0")
            .css("cursor", "pointer")
            .hide()
            .appendTo($("body"))
        ;

        fetchTalkback(function(suggestion) {
            d.click(function() {
                showSuggestion(suggestion);
            })
            d.contextmenu(function() {
                showSuggestion(suggestion, true);
                return false;
            })
            d.fadeIn(350);
        });
    });

    function fetchTalkback(callback) {
        console.log("TALKBACKER DEBUG:\n" +
            "resource hint: " + injected_variables['resource_hint'] + "\n" +
            "url: " + document.location.href
        );
        if (is_article()) {
            var article_id = get_article_id();
            console.log("ARTICLE!");
            // Do the big ass cross-site scripting
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "http://talkbacker.dev.meginon.com:5000/talkbacks/" + article_id, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    // JSON.parse does not evaluate the attacker's scripts.
                    var response = JSON.parse(xhr.responseText);
                    console.log("RESP: " + response);
                    console.log("talkback: " + response.talkback);
                    callback(response);
                }
            };
            xhr.send();
        }
    }

    function showSuggestion(response, show_all) {
        var single_talkback_line = response.talkback
        var multi_talkback_line = response.talkback_list.join("\n\n");
        if (show_all == true) {
            var text = multi_talkback_line;
        }
        else {
            var text = single_talkback_line;
        }

        swal({
            title: "טוקבק עסיסי - משדרג כל כתבה!",
            text: text,
            imageUrl: injected_variables.messagebox_image,
        });
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
}());