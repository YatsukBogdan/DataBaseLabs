# MongoDB  (JS)
```
redisClient.get('word', (err, word) => {
    if (word && req.params.word && word == req.params.word) {
      redisClient.get('users', (err, users) => {
        logMessage('Redis in action');
        var users_res = JSON.parse(users);
        logMessage(users);
        logMessage(users_res);
        res.json(users_res);
      });
    }...```
