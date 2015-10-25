
var AlarmForm = React.createClass({
        toLabel: function(day) {
                return (<label className="btn btn-default">
                                <input type="checkbox" value={day}>
                                {day}
                                </input>
                                </label>);
        },
        render : function() {
                return (<div>
                                <div className="btn-group" data-toggle="buttons">
                                {
                                        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].map(this.toLabel)
                                }
                                </div>
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
