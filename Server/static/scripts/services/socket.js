'use strict';

angular.module('webApp')
    .factory('socket', function (socketFactory) {
        var socket = socketFactory({
            ioSocket: io.connect('/control')
        });
        socket.forward('error');
        return socket;
    });