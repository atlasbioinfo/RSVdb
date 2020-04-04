

function showOthers() {
    if ($("#labmore").text() == "[more...]") {
        $("#labmore").text("[less...]");
        $("#otherAbs").attr("style", "visibility: visible;");
    } else {
        $("#labmore").text("[more...]");
        $("#otherAbs").attr("style", "visibility: hidden;display: none;");
    }
};

Back2top.init();