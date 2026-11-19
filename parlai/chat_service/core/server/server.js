/* Copyright (c) Facebook, Inc. and its affiliates.
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
'use strict';

const bodyParser = require('body-parser');
const express = require('express');
const fs = require('fs');
const http = require('http');
const https = require('https');
const nunjucks = require('nunjucks');
const WebSocket = require('ws');

const task_directory_name = 'task';

const PORT = process.env.PORT || 3000;
const LOCAL_HTTPS = process.env.LOCAL_HTTPS || false;
const HOME = process.env.HOME || '';

// Initialize app
const app = express();
app.use(function(req, res, next) {
  const port = server.address().port;
  if (!['127.0.0.1:' + port, 'localhost:' + port].includes(req.headers.host) || req.headers.origin) {
    res.sendStatus(403); return;
  }
  next();
});
app.use(bodyParser.text({ limit: '64kb' }));
app.use(
  bodyParser.urlencoded({
    extended: false,
    limit: '64kb',
    parameterLimit: 100,
  })
);
app.use(bodyParser.json({ limit: '64kb' }));

nunjucks.configure(task_directory_name, {
  autoescape: true,
  express: app,
});

// ======================= <Socket> =======================

// Start a socket to make a connection between the world and
let server;
if (LOCAL_HTTPS) {
  var options = {
      ca: fs.readFileSync(HOME + '/.ssl/fullchain.pem'),
      key: fs.readFileSync(HOME + '/.ssl/privkey.pem'),
      cert: fs.readFileSync(HOME + '/.ssl/cert.pem'),
  };

  server = https.createServer(options, app);
} else {
  server = http.createServer(app);
}
const wss = new WebSocket.Server({
  server, maxPayload: 65536, perMessageDeflate: false,
  verifyClient: function(info, done) {
    const port = server.address().port;
    const allowed = ['127.0.0.1:' + port, 'localhost:' + port];
    done(allowed.includes(info.req.headers.host) && !info.origin, 403);
  },
});

// Socket used for speaking to the world
var world_socket = null;

// Handles sending a message through the socket
function _send_message(event_name, event_data) {
  if (world_socket) {
    var packet = {
      type: event_name,
      content: event_data,
    };
    world_socket.send(JSON.stringify(packet), function ack(error) {
      if (error === undefined) {
        return true;
      }
      console.log('Ran into error trying to send, retrying');
      setTimeout(function() {
        world_socket.send(JSON.stringify(packet), function ack2(error2) {
          if (error2 === undefined) {
            return true;
          }
          console.log('Repeat send of packet failed');
          console.log(packet);
          console.log(error2);
        });
      }, 500);
    });
    return true;
  } else {
    console.log('Message recieved without world connected');
    console.log(event_data);
    return false;
  }
}

// Register handlers
wss.on('connection', function(socket) {
  console.log('Client connected');
  // Disconnects are logged
  socket.on('disconnect', function() {
    console.log('World disconnected');
  });

  socket.on('message', function(data) {
    try { data = JSON.parse(data.toString()); }
    catch (error) { socket.close(1007, 'Invalid JSON'); return; }
    if (!data || typeof data !== 'object' || Array.isArray(data)) {
      socket.close(1007, 'Expected an object'); return;
    }
    if (data['type'] == 'world_alive') {
      world_socket = socket;
    } else if (data['type'] == 'ping') {
      socket.send(JSON.stringify({ type: 'pong', content: 'pong' }));
    }
  });

  socket.on('error', err => {
    console.log('Caught socket error');
    console.log(err);
  });

  socket.send(
    JSON.stringify({ type: 'conn_success', content: 'Socket is open!' }),
    function ack(error) {
      return;
    }
  );
});

server.listen(PORT, '127.0.0.1', function() {
  console.log('Listening on %d', server.address().port);
});

// Messenger requires a separately maintained, authenticated integration.
app.all('/webhook', function(req, res) {
  res.status(410).send('Messenger integration is unavailable in this local runtime.');
});
