const daysOfWeek = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"];

var AlarmForm = React.createClass({
        toDayLabel: function(day) {
                return (<label key={day} className="btn btn-default">
                                <input type="checkbox" value={day} name={day} id={day}>
                                {day}
                                </input>
                                </label>);
        },
        render : function() {
                return (<div>
                                <form id="set-form" role="form-inline"> 
                                <div className="form-group">
                                <div className="input-group bootstrap-timepicker timepicker">
                                <input id="timepicker" name="time" type="text" className="text-center input-lg"></input>
                                </div>
                                </div>

                                <div className="form-group">
                                <div id="daysOfWeek" className="btn-group" data-toggle="buttons" id="dayOfWeek">
                                {
                                        daysOfWeek.map(this.toDayLabel)
                                }
                                </div>
                                </div>

                                </form>

                                </div>);
        },
        componentDidMount: function() {
                $("#timepicker").timepicker();
        }
});



var App  = React.createClass({

        render: function() {
                return (<div>
                                <center>
                                <h2>Rise and Shine</h2>
                                <AlarmForm/>

                                <div className="form-group">
                                <div className="btn-group-vertical">
                                <button ref="stat" onClick={this.stat} className="btn btn-default">Status</button>
                                </div>
                                </div>

                                <div className="form-group">
                                <div className="btn-group-vertical">
                                <button ref="set"  onClick={this.set} className="btn btn-default">Set alarm</button>
                                <button ref="unset" onClick={this.reset} className="btn btn-default">Cancel alarm</button>
                                </div>
                                </div>

                                <div className="form-group">
                                <div className="btn-group-vertical">
                                <button ref="on" onClick={this.on} className="btn btn-default">Turn on lights</button>
                                <button ref="off" onClick={this.off} className="btn btn-default">Turn off lights</button>
                                <button ref="test" onClick={this.test} className="btn btn-default">Animation</button>
                                </div>
                                </div>
                                </center>

                                </div>)
        },

        test: function() {
                console.log("testing");
                $.get("/test", function(result) {
                        const OK = result.status == "OK";
                        alert("Testing lights "+ OK);
                });
        },

        set: function() {
                const data  = {"time": $("#timepicker").val()};
                const checked = $(":checked");
                if (checked.length == 0) {
                    alert("Select at least one day of the week");
                    return;
                } 
                for (var i=0; i < checked.length; i++) {
                        var v = checked[i].value;
                        data[v]=  v;
                }
                console.log("setting "+ JSON.stringify(data));

                $.get("/set", data, function(result) {
                        console.log("set result"+ JSON.stringify(result));
                        const OK = result.status == "OK";
                        alert("Set alarm "+ OK);
                });
        },

        on: function() {
                console.log("turning on");
                $.get("/on", function(result) {
                        alert("turned on");
                });
        }, 

        off: function() {
                console.log("turning off");
                $.get("/off", function(result) {
                        alert("turned off");
                });
        }, 

        reset: function() {
                console.log("reset");
                $.get("/reset", function(result) {
                        const OK = result.status == "OK";
                        alert("Alarm cancelled "+ OK);
                });
        }, 
        stat: function() {
                console.log("stat");
                $.get("/stat", function(result) {
                        console.log(JSON.stringify(result));
                        const stat = result.stat;
                        const msg =  result.status == "None" ? "Alarm not set" : "Alarm time : " + stat.time +"\nAlarm days : "+ stat.weekdays;
                        alert(msg);
                });
        }, 
        addMusic: function() {
                console.log("adding music");
                //TODO
        } 
});

React.render(
                <App/>,
                document.getElementById("content") 
            );
