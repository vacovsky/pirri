function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
};

function populateCalEvents() {
    var result = [{
        id: 'E01',
        title: 'Meeting with BA',
        start: '2016-10-15 10:30:00',
        end: '2016-10-15 13:00:00',
        backgroundColor: '#12CA6B',
        textColor: '#FFF'
    }, {
        id: 'E02',
        title: 'Lunch',
        start: '2016-10-15 13:15:00',
        end: '2016-10-15 14:30:00',
        backgroundColor: '#12CA6B',
        textColor: '#FFF'
    }, {
        id: 'E03',
        title: 'Customer Appointment',
        start: '2016-10-15 09:00:00',
        end: '2016-10-15 09:30:00',
        backgroundColor: '#AA3322',
        textColor: '#FFF'
    }];

    $.get('/schedule/cal'), function(data) {
        result = data;
    };
    //setTimeout(function() {result = angular.element(document.getElementById('PirriControl')).scope().calList}, 1000);
    return result;
}