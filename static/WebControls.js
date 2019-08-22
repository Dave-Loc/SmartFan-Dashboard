//On page load
$(document).ready(function() {
    document.getElementById("AdvancedSpeedInput").style.visibility = "hidden";
    document.getElementById("DefaultSpeedInput").style.visibility = "hidden";
    //On fan toggle switch change
    $("#FanPowerCheck").change(function() {
        if ($(this).prop("checked")) {
            $.ajax({
                type: "POST",
                url: "/FanSpeedOn",
                success: function(status) {
                }
            });
        document.getElementById("AdvancedSpeedInput").style.visibility = "visible";
        document.getElementById("DefaultSpeedInput").style.visibility = "visible";
        } else {
            $.ajax({
                type: "POST",
                url: "/FanSpeedOff",
                success: function(status) {
                }
            });
            document.getElementById("AdvancedSpeedInput").style.visibility = "hidden";
            document.getElementById("DefaultSpeedInput").style.visibility = "hidden";
        }
    });
    //Hide fan oscillation input control
    document.getElementById("FanRotationInput").style.visibility = "hidden";
    //On fan oscillation toggle switch change
    $("#FanRotationPower").change(function() {
        if ($(this).prop("checked")) {
            //Show fan oscillation input control
            document.getElementById("FanRotationInput").style.visibility = "visible";
            $.ajax({
                type: "POST",
                url: "/FanRotationOn",
                success: function(status) {
                }
            });
        } else {
            //Hide fan oscillation input control
            document.getElementById("FanRotationInput").style.visibility = "hidden";
            $.ajax({
                type: "POST",
                url: "/FanRotationOff",
                success: function(status) {
                }
            });
        }
    });
        //Initially hide advanced speed settings
        document.getElementById("FanSpeedInput").style.visibility = "hidden";
        //On advanced speed settings turned on
    $("#AdvancedFanSpeedInput").change(function() {
        if ($(this).prop("checked")) {
            //Show fan speed input control bar
            document.getElementById("FanSpeedInput").style.visibility = "visible";
            //Set the default value of the speed input control bar to 100
            $('#FanSpeedControl').val(100);
        } else {
            //Hide fan speed input control bar
            document.getElementById("FanSpeedInput").style.visibility = "hidden";
        }
    });



});
    //On fan oscillation input control change
    function ChangeFanRotation() {
        $.ajax({
            type: "POST",
            url: "/GetWebFanRotation",
            data: {
                FanRotation: $('#FanRotation').val()
            },
            success: function(data) {
                console.log(data);
            }
        });
    }
//Changing fan speed function
function ChangeFanSpeed() {
    $.ajax({
        type: "POST",
        url: "/GetWebFanDutyCycle",
        data: {
            FanDutyCycle: $('#FanSpeedControl').val()
        },
        success: function(data) {
            console.log(data);
        }
    });
}

//Changing fan speed function
function ChangeFanSpeedLow() {
    $.ajax({
        type: "POST",
        url: "/GetWebFanDutyCycle",
        data: {
            FanDutyCycle: 40
        },
        success: function(data) {
            console.log(data);
            $('#FanSpeedControl').val(40);
        }
    });
}

//Changing fan speed function
function ChangeFanSpeedMed() {
    $.ajax({
        type: "POST",
        url: "/GetWebFanDutyCycle",
        data: {
            FanDutyCycle: 70
        },
        success: function(data) {
            console.log(data);
            $('#FanSpeedControl').val(70);
        }
    });
}

//Changing fan speed function
function ChangeFanSpeedHigh() {
    $.ajax({
        type: "POST",
        url: "/GetWebFanDutyCycle",
        data: {
            FanDutyCycle: 100
        },
        success: function(data) {
            console.log(data);
            $('#FanSpeedControl').val(100);
        }
    });
}

function output(){
    w = document.getElementById("month").value;
    x = document.getElementById("day").value;
    y = document.getElementById("year").value;
    z = document.getElementById("tim").value;
	
   document.getElementById("time-output").innerHTML = w + " " + x + "," + " " + y + " "+ z;
}

function tempOut(){
    a = document.getElementById("temperature").value;
    b = document.getElementById("humid").value;
    c = document.getElementById("airpress").value;

    if( a != " "){
        document.getElementById("result").innerHTML = "Fan will turn on at " + a + "&#37;" ;
    }
    
}
