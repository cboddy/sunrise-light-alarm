var App  = React.createClass({

        render: function() {
                return (<div>
                                <p>Hello World</p>
                                </div>)
        }
});

React.render(
                <App/>,
                document.getElementById("content") 
            );
