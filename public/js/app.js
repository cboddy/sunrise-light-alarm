
var AlarmForm = React.createClass({
        toDayLabel: function(day) {
                return (<label className="btn btn-default">
                                <input type="checkbox" value={day}>
                                {day}
                                </input>
                                </label>);
        },
        componentDidMount: function() {
                $("#timepicker").timepicker();
        },
        render : function() {
                return (<div className="col-sm-6">
                                <center>
                                <form >
                                <div className="control-group">
                                <label htmlFor="timepicker-wrapper" className="col-sm-3 control-label">Alarm time</label>
                                <div id="timepicker-wrapper" className="bootstrap-timepicker timepicker col-sm-9">
                                <input id="timepicker" type="text" className="form-control text-center input-lg">
                                </input>
                                </div>
                                </div>

                                <div className="control-group">
                                <label htmlFor="daysOfWeek" className="col-sm-3 control-label">Days of week</label>
                                <div id="daysOfWeek" className="col-sm-9 btn-group" data-toggle="buttons" id="dayOfWeek">
                                {
                                        ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"].map(this.toDayLabel)
                                }
                                </div>
                                </div>
                                <div className="control-group">
                                <button  type="submit" className="btn btn-default">Set alarm</button>
                                </div>
                                </form>
                                </center>
                                </div>);
        }
});



var App  = React.createClass({

        render: function() {
                return (<div>
                                <AlarmForm/>
                                </div>)
        }
});

React.render(
                <App/>,
                document.getElementById("content") 
            );
