
var AlarmForm = React.createClass({
        toDayLabel: function(day) {
                return (<label key={day} className="btn btn-default">
                                <input type="checkbox" value={day}>
                                {day}
                                </input>
                                </label>);
        },
        componentDidMount: function() {
                $("#timepicker").timepicker();
        },
        render : function() {
                return (<div>
                                <form role="form-inline" action="/set" method="get"> 
                                <div className="form-group">
                                <div className="input-group bootstrap-timepicker timepicker">
                                <input id="timepicker" type="text" className="text-center input-lg"></input>
                                </div>
                                </div>

                                <div className="form-group">
                                <div id="daysOfWeek" className="btn-group" data-toggle="buttons" id="dayOfWeek">
                                {
                                        ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"].map(this.toDayLabel)
                                }
                                </div>
                                </div>

                                <button  type="submit" className="btn btn-default">Set alarm</button>
                                </form>

                                </div>);
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
                        alert("Testing lights");}
                     );
        }, 
        reset: function() {
                console.log("reset");
        }, 
        addMusic: function() {
                console.log("adding music");
        } 

});

React.render(
                <App/>,
                document.getElementById("content") 
            );
