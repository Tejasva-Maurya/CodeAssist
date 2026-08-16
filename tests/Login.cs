using System;

namespace Frontend {
    class LoginController {
        // Handle user login
        public void HandleLogin() {
            AuthService.Authenticate();
            Console.WriteLine("Logged in!");
        }
    }
}
