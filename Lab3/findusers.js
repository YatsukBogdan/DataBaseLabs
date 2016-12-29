var express = require('express');
var router = express.Router();
var path = require('path');
var md5 = require('js-md5');
var user = require('../databaseutils').user;

var redisClient = require('redis').createClient();

const LOG_PREFIX = 'FIND_USER ROUTE';
function getCurrentTime() {
    return new Date().toTimeString().replace(/.*(\d{2}:\d{2}:\d{2}).*/, "$1");
}
function logMessage(msg) {
  console.log(getCurrentTime() + '     ' + LOG_PREFIX + '     ' + msg);
}

router.get('/:word', (req, res) => {
  redisClient.get('word', (err, word) => {
    if (word && req.params.word && word == req.params.word) {
      redisClient.get('users', (err, users) => {
        logMessage('Redis in action');
        var users_res = JSON.parse(users);
        logMessage(users);
        logMessage(users_res);
        res.json(users_res);
      });
    } else if (req.params.word) {
      redisClient.set('word', req.params.word);
      logMessage('Word requested: ' + req.params.word);
      user.find({
        username: {
          $regex: req.params.word
        }
      }, (err, users) => {
        if (err) {
          logMessage('Database error: ' + err);
          res.json({error: 'database error'});
          return;
        }
        if (users) {
          var users_res = [];
          for (var i = 0; i < users.length; i++){
            users_res.push({
              username: users[i].username
            });
          }
          logMessage('Users in response: ' + users_res);
          res.json(users_res);

          redisClient.set('users', JSON.stringify(users));
          logMessage('Redis saved users');
        } else {
          logMessage('No users found');
          res.json({});
        }
      });
    } else {
      logMessage('Word to find missing in request body');
      res.json({
        error: 'Word to find missing in request body'
      });
    }
  });
});

module.exports = router;
