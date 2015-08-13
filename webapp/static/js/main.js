var connection = new autobahn.Connection({
   url: 'ws://127.0.0.1:8080/ws',
   realm: 'frontend'}
);

connection.onopen = function (session) {

   session.call('utcnow').then(
      function (now) {
         console.log("Current time:", now);
         connection.close();
      },
      function (error) {
         console.log("Call failed:", error);
         connection.close();
      }
   );
};

connection.open();
