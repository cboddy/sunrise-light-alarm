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

                                <button  type="submit" className="btn btn-default">Set alarm</button>
                                </form>

                                </div>);
        },
        componentDidMount: function() {
                $("#timepicker").timepicker();
                $("#set-form").submit(function(event) {
                        event.preventDefault();
                        const data  = {"time": $("#timepicker").val()};
                        const checked = $(":checked");
                        for (var i=0; i < checked.length; i++) {
                                var v = checked[i].value;
                                data[v]=  v;
                        }
                        $.get("/set", data, function(result) {

                                console.log("set result"+ JSON.stringify(result));
                                const OK = result.status == "OK";
                                alert("Set alarm "+ OK);
                        });
                });
        }
});



var App  = React.createClass({

        render: function() {
                return (<div>
                                <center>
                                <h2>Rise and Shine</h2>
                                <AlarmForm/>
                                <div className="btn-group-vertical">
                                <button ref="unset" className="btn btn-default">Un-set alarm</button>
                                <button ref="test" onClick={this.test} className="btn btn-default">Test-lights</button>
                                <button ref="addMusic" className="btn btn-default">Add music</button>
                                </div>
                                </center>

                                </div>)
        },

        test: function() {
                console.log("testing");
                $.get("/test", function() {
                        const OK = result.status == "OK";
                        alert("Testing lights "+ OK);
                });
        }
        , 
        reset: function() {
                console.log("reset");
                $.get("/reset", function() {
                        const OK = result.status == "OK";
                        alert("Un-set alarm "+ OK);
                });
        }, 
        addMusic: function() {
                console.log("adding music");
        } 

});

React.render(
                <App/>,
                document.getElementById("content") 
            );
